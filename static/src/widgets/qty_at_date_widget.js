/** @odoo-module **/

import { QtyAtDateWidget } from "@sale_stock/widgets/qty_at_date_widget";
import { patch } from "@web/core/utils/patch";

patch(QtyAtDateWidget.prototype, {
  showPopup(ev) {
    this.updateCalcData();

    let warehouseStockInfo = [];
    const rawData = this.props.record.data.warehouse_stock_info;
    if (rawData) {
      try {
        warehouseStockInfo = JSON.parse(rawData);
      } catch (e) {
        console.warn("Failed to parse warehouse_stock_info:", e);
      }
    }

    this.popover.open(ev.currentTarget, {
      record: this.props.record,
      calcData: this.calcData,
      warehouseStockInfo: warehouseStockInfo,
    });
  },
});
