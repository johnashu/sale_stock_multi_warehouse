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
        "product_id",
        "product_uom_qty",
        "scheduled_date",
        "warehouse_id",
        "order_id.warehouse_id",
        "order_id.company_id",
        "order_id.commitment_date",
        "display_qty_widget",
        "free_qty_today",
        "qty_available_today",
        "virtual_available_at_date",
    )
    def _compute_warehouse_stock_info(self):
        """Compute stock availability for all warehouses as JSON data."""
        lines_to_compute = self.filtered(
            lambda l: l.product_id and l.display_qty_widget
        )
        lines_without_product = self - lines_to_compute

        for line in lines_without_product:
            line.warehouse_stock_info = "[]"

        if not lines_to_compute:
            return

        # Use the same delivery date as sale_stock's _compute_qty_at_date so
        # forecasted figures are evaluated at the same point in time.
        now = fields.Datetime.now()
        line_keys = {
            line: (
                line.order_id.company_id.id or self.env.company.id,
                line.order_id.commitment_date or line._expected_date() or now,
            )
            for line in lines_to_compute
        }

        # Batch lines by (company, forecast date) so quantities are read once per
        # group, mirroring sale_stock's _compute_qty_at_date grouping.
        grouped_lines = defaultdict(lambda: self.env["sale.order.line"])
        for line in lines_to_compute:
            grouped_lines[line_keys[line]] |= line

        warehouses_by_company = {}
        warehouse_info = {}
        stock_cache = defaultdict(dict)

        for (company_id, scheduled_date), lines in grouped_lines.items():
            warehouses = warehouses_by_company.get(company_id)
            if warehouses is None:
                warehouses = self.env["stock.warehouse"].search(
                    [("company_id", "=", company_id)]
                )
                warehouses_by_company[company_id] = warehouses
                for wh in warehouses:
                    warehouse_info[wh.id] = {"name": wh.name, "code": wh.code}

            products = lines.mapped("product_id")
            for warehouse in warehouses:
                # Odoo 18 scopes product quantities via the context key
                # 'warehouse_id' (not 'warehouse'); without it, reads return
                # company-wide totals identical for every warehouse.
                products_with_context = products.with_context(
                    to_date=scheduled_date,
                    warehouse_id=warehouse.id,
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
                    stock_cache[(company_id, scheduled_date, warehouse.id)][
                        product_data["id"]
                    ] = {
                        "qty_available": product_data["qty_available"],
                        "free_qty": product_data["free_qty"],
                        "virtual_available": product_data["virtual_available"],
                    }

        for line in lines_to_compute:
            product_id = line.product_id.id
            company_id, scheduled_date = line_keys[line]
            current_warehouse_id = line.warehouse_id.id if line.warehouse_id else False
            use_line_qty_fields = line.state in ("draft", "sent")

            stock_data = []
            for warehouse in warehouses_by_company.get(
                company_id, self.env["stock.warehouse"]
            ):
                wh_stock = stock_cache.get(
                    (company_id, scheduled_date, warehouse.id), {}
                ).get(product_id, {})

                is_current = warehouse.id == current_warehouse_id
                if is_current and use_line_qty_fields:
                    # Reuse sale_stock's line-level figures so the current
                    # warehouse row matches the standard availability popup.
                    free_qty = line.free_qty_today
                    virtual_available = line.virtual_available_at_date
                    qty_available = line.qty_available_today
                else:
                    qty_available = wh_stock.get("qty_available", 0)
                    free_qty = wh_stock.get("free_qty", 0)
                    virtual_available = wh_stock.get("virtual_available", 0)
                    if line.product_uom and line.product_id.uom_id and line.product_uom != line.product_id.uom_id:
                        qty_available = line.product_id.uom_id._compute_quantity(
                            qty_available, line.product_uom
                        )
                        free_qty = line.product_id.uom_id._compute_quantity(
                            free_qty, line.product_uom
                        )
                        virtual_available = line.product_id.uom_id._compute_quantity(
                            virtual_available, line.product_uom
                        )

                has_stock = (
                    qty_available != 0 or free_qty != 0 or virtual_available != 0
                )

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
