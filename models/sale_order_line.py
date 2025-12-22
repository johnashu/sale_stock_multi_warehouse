# -*- coding: utf-8 -*-
import json
from collections import defaultdict

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warehouse_stock_info = fields.Text(
        compute="_compute_warehouse_stock_info",
        string="Warehouse Stock Info",
        help="JSON data containing stock information for all warehouses",
    )

    @api.depends(
        "product_id", "scheduled_date", "order_id.warehouse_id", "display_qty_widget"
    )
    def _compute_warehouse_stock_info(self):
        """Compute stock availability for all warehouses as JSON data."""
        all_warehouses = self.env["stock.warehouse"].search([])

        if not all_warehouses:
            for line in self:
                line.warehouse_stock_info = "[]"
            return

        lines_to_compute = self.filtered(
            lambda l: l.product_id and l.display_qty_widget
        )
        lines_without_product = self - lines_to_compute

        for line in lines_without_product:
            line.warehouse_stock_info = "[]"

        if not lines_to_compute:
            return

        product_ids = lines_to_compute.mapped("product_id").ids
        products = self.env["product.product"].browse(product_ids)

        stock_cache = defaultdict(dict)

        scheduled_date = fields.Datetime.now()

        for warehouse in all_warehouses:
            products_with_context = products.with_context(
                to_date=scheduled_date, warehouse=warehouse.id
            )
            product_data_list = products_with_context.read(
                [
                    "id",
                    "qty_available",
                    "free_qty",
                    "virtual_available",
                ]
            )

            for product_data in product_data_list:
                stock_cache[warehouse.id][product_data["id"]] = {
                    "qty_available": product_data["qty_available"],
                    "free_qty": product_data["free_qty"],
                    "virtual_available": product_data["virtual_available"],
                }

        warehouse_info = {
            wh.id: {"name": wh.name, "code": wh.code} for wh in all_warehouses
        }

        for line in lines_to_compute:
            product_id = line.product_id.id
            current_warehouse_id = line.warehouse_id.id if line.warehouse_id else False

            stock_data = []
            for warehouse in all_warehouses:
                wh_stock = stock_cache.get(warehouse.id, {}).get(product_id, {})

                qty_available = wh_stock.get("qty_available", 0)
                free_qty = wh_stock.get("free_qty", 0)
                virtual_available = wh_stock.get("virtual_available", 0)

                has_stock = (
                    qty_available != 0 or free_qty != 0 or virtual_available != 0
                )
                is_current = warehouse.id == current_warehouse_id

                if has_stock or is_current:
                    stock_data.append(
                        {
                            "warehouse_id": warehouse.id,
                            "warehouse_name": warehouse_info[warehouse.id]["name"],
                            "warehouse_code": warehouse_info[warehouse.id]["code"],
                            "qty_available": qty_available,
                            "free_qty": free_qty,
                            "virtual_available": virtual_available,
                            "is_current": is_current,
                        }
                    )

            # Sort: current warehouse first, then by name
            stock_data.sort(key=lambda x: (not x["is_current"], x["warehouse_name"]))
            line.warehouse_stock_info = json.dumps(stock_data)
