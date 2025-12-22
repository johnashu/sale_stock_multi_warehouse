# -*- coding: utf-8 -*-
{
    "name": "Sale Stock Multi-Warehouse Availability",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "summary": "Show stock availability from all warehouses in Sales Order popup",
    "description": """
Sale Stock Multi-Warehouse Availability
=======================================

This module extends the stock availability popup in Sales Order lines to show
stock information from ALL warehouses, not just the warehouse selected on the
Sales Order.

Features:
- Shows a breakdown of stock per warehouse in the availability popup
- Displays Available and Forecasted quantities for each warehouse
- Highlights the current order's warehouse
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
