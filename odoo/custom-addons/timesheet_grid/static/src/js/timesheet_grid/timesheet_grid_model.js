odoo.define('timesheet_grid.GridModel', function (require) {
    "use strict";

    const { _t } = require('web.core');
    const GridModel = require('web_grid.GridModel');

    const TimesheetGridModel = GridModel.extend({
        /**
         * @override
         */
        async reload(handle, params) {
            if (params && 'groupBy' in params) {
                // With timesheet grid, it makes nonsense to manage group_by with a field date (as the dates are already in the rows).
                // Detection of groupby date with ':' (date:day). Ignore grouped by date, and display warning.
                var GroupBy = params.groupBy.filter(filter => {
                    return filter.split(':').length === 1;
                });
                if (GroupBy.length !== params.groupBy.length) {
                    this.do_warn(false, _t('Grouping by date is not supported'));
                }
                params.groupBy = GroupBy;
            }
            return this._super(...arguments);
        },
        /**
         * @private
         * @param {string[]} groupBy
         * @returns {Promise}
         */
        _fetchGroupedData: async function (groupBy) {
            const d = await this.dp.add(this._rpc({
                model: this.modelName,
                method: 'read_grid_domain',
                kwargs: {
                    field: this.colField,
                    range: this.currentRange,
                },
                context: this.getContext(),
            }));
    
            const groups = await this.dp.add(this._rpc({
                model: this.modelName,
                method: 'read_group',
                kwargs: {
                    domain: d.concat(this.domain || []),
                    fields: [this.sectionField],
                    groupby: [this.sectionField],
                },
                context: this.getContext()
            }));
    
            let prom;
            if (!groups.length) {
                // if there are no groups in the output we still need
                // to fetch an empty grid so we can render the table's
                // decoration (pagination and columns &etc) otherwise
                // we get a completely empty grid
                prom = Promise.all([this._fetchSectionGrid(groupBy, {
                    __domain: this.domain || [],
                })]);
            } else {
                prom = Promise.all((groups || []).map(group => {
                    return this._fetchSectionGrid(groupBy, group);
                }));
            }
            const results = await this.dp.add(prom);
            // we will not check the columns equality as they could be different
            // from employee to another based on the callOn-duty
            /*if (!(_.isEmpty(results) || _.reduce(results, function (m, it) {
                    return _.isEqual(m.cols, it.cols) && m;
                }))) {
                throw new Error(_t("The sectioned grid view can't handle groups with different columns sets"));
            }*/
            results.forEach((group, groupIndex) => {
                results[groupIndex].totals = this._computeTotals(group.grid, group.rows);
                group.rows.forEach((row, rowIndex) => {
                    const { id, label } = this._getRowInfo(row, true);
                    results[groupIndex].rows[rowIndex].id = id;
                    results[groupIndex].rows[rowIndex].label = label;
                });
            });
    
            this._gridData = {
                isGrouped: true,
                data: results,
                totals: this._computeTotals(_.flatten(_.pluck(results, 'grid'), true), _.flatten(_.pluck(results, 'rows'), true)),
                groupBy,
                colField: this.colField,
                cellField: this.cellField,
                range: this.currentRange.name,
                context: this.context,
            };
        },




    });

    return TimesheetGridModel;
});
