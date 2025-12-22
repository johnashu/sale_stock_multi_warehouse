# Sale Stock Multi-Warehouse Availability

An Odoo 17 module that extends the stock availability popup in Sales Order lines to display stock information from all warehouses, not just the warehouse selected on the order.

**Author:** John Ashurst  
**Company:** SJR Nebula  
**License:** LGPL-3  
**Version:** 17.0.1.0.0

---

## Overview

In standard Odoo, when you click on the stock availability indicator on a Sales Order line, you only see stock information for the warehouse assigned to that order. This can be limiting for businesses operating multiple warehouses who need visibility into stock availability across their entire inventory.

This module enhances the stock availability popup to show a complete breakdown of stock levels per warehouse, allowing sales teams to make informed decisions about order fulfillment without leaving the Sales Order screen.

---

## Features

* **Multi-Warehouse Stock Display**: View stock availability from all warehouses in a single popup
* **Per-Warehouse Breakdown**: See Available and Forecasted quantities for each warehouse
* **Current Warehouse Highlighting**: The warehouse assigned to the order is clearly marked and displayed first
* **Aggregated Totals**: View total available and forecasted stock across all warehouses
* **Smart Filtering**: Only warehouses with stock (or the current order warehouse) are displayed
* **Color-Coded Quantities**: Positive quantities shown in green, zero/negative in red for quick visual assessment
* **Non-Intrusive**: Extends the existing popup without altering standard Odoo workflows

---

## Screenshots

The enhanced popup displays:

| Warehouse | Available | Forecasted |
|-----------|-----------|------------|
| Main Warehouse (Current) | 50 | 75 |
| Secondary Warehouse | 25 | 30 |
| **TOTAL (All Warehouses)** | **75** | **105** |

---

## Technical Details

### Dependencies

* `sale_stock` (Odoo core module)

### Components

**Backend (Python)**
* Extends `sale.order.line` with a computed field `warehouse_stock_info`
* Calculates stock availability (qty_available, free_qty, virtual_available) for all warehouses
* Uses efficient batch processing with caching to minimize database queries

**Frontend (JavaScript)**
* Patches the standard `QtyAtDateWidget` from `sale_stock`
* Parses warehouse stock data and passes it to the popover component

**Template (XML)**
* Extends `QtyAtDatePopover` to display the warehouse-by-warehouse breakdown table
* Includes styling for current warehouse highlighting and color-coded quantities

---

## Installation

1. Clone or download this module to your Odoo addons directory
2. Update the addons list in Odoo (Apps menu > Update Apps List)
3. Search for "Sale Stock Multi-Warehouse Availability" and install

---

## Configuration

No configuration required. Once installed, the enhanced stock popup is automatically available on all Sales Order lines.

---

## Usage

1. Open a Sales Order
2. Add a product line (or view an existing one)
3. Click on the stock availability indicator (the widget showing forecasted dates/quantities)
4. The popup will now display stock information for all warehouses

---

## Compatibility

* **Odoo Version:** 17.0
* **Edition:** Community and Enterprise

---

## Support

For issues, feature requests, or contributions, please contact SJR Nebula.

---

## Changelog

### 17.0.1.0.0

* Initial release
* Multi-warehouse stock display in Sales Order line popup
* Warehouse highlighting and totals aggregation
