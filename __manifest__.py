# -*- coding: utf-8 -*-
{
    "name": "Sale Stock Multi-Warehouse Availability",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "summary": "Show stock availability from all warehouses in Sales Order popup",
    "description": """
Sale Stock Multi-Warehouse Availability
=======================================

This module extends the stock availability popup in Sales Order lines to display
stock information from ALL warehouses, not just the warehouse selected on the
Sales Order. It enables sales teams to make informed fulfillment decisions by
providing complete visibility into inventory across the entire warehouse network.

Features
--------
* Multi-warehouse stock display in a single popup
* Per-warehouse breakdown of Available and Forecasted quantities
* Current order warehouse highlighted and displayed first
* Aggregated totals across all warehouses
* Smart filtering to show only warehouses with stock
* Color-coded quantities for quick visual assessment
* Non-intrusive extension of standard Odoo workflows

Technical Details
-----------------
* Extends sale.order.line with computed warehouse stock data
* Patches the QtyAtDateWidget frontend component
* Uses efficient batch processing with caching for performance

Author: John Ashurst
Company: SJR Nebula
    """,
    "author": "SJR Nebula",
    "depends": ["sale_stock"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sale_stock_multi_warehouse/static/src/widgets/*.xml",
            "sale_stock_multi_warehouse/static/src/widgets/*.js",
        ],
    },
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
