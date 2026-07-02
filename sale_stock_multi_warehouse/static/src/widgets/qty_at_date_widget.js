/** @odoo-module **/

import {
    QtyAtDatePopover,
    QtyAtDateWidget,
} from "@sale_stock/widgets/qty_at_date_widget";
import { patch } from "@web/core/utils/patch";

export class QtyAtDatePopoverMultiWarehouse extends QtyAtDatePopover {
    static template = "sale_stock_multi_warehouse.QtyAtDatePopover";
    static props = {
        record: Object,
        calcData: Object,
        close: Function,
        warehouseStockInfo: { type: Array, optional: true },
    };
}

patch(QtyAtDateWidget, {
    components: {
        ...QtyAtDateWidget.components,
        Popover: QtyAtDatePopoverMultiWarehouse,
    },
});

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
