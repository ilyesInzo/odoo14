var employee_data = {}
odoo.define("magenest_org_chart.org_chart_employee_v2", function (require) {
    "use strict";
    var tags = {};
    var core = require('web.core');
    var ajax = require('web.ajax');
    var AbstractAction = require('web.AbstractAction');
    var QWeb = core.qweb;
    var OrgChartEmployee = AbstractAction.extend({
        template: "magenest_org_chart.get_org_chart_employee_template",
        jsLibs: [
            '/magenest_org_chart/static/js/jquery.orgchart.js'
        ],
        init: function (parent, context) {
            this._super(parent, context);
            var self = this;
            if (context.tag == 'org_chart_employee_v2') {
                self._rpc({
                    model: 'hr.employee',
                    method: 'get_employee_data_v2',
                }).then(function (result) {
                    console.log(result)
                    employee_data = result
                    self.render();
                });
                this.href = window.location.href;
            }
        },

        willStart: function () {
            return $.when(ajax.loadLibs(this), this._super());
        },
        start: function () {
            var self = this;
            return this._super();
        },
        render: function () {
            this._super;
            var self = this;
            var org_chart = QWeb.render('magenest_org_chart.get_org_chart_employee_template', {});
            // console.log(this)
            $(".o_control_panel").addClass("o_hidden");
            return org_chart;
        },
        reload: function () {
            window.location.href = this.href;
        }
    });

    core.action_registry.add('org_chart_employee_v2', OrgChartEmployee);
    return {
        OrgChartEmployee: OrgChartEmployee
    };

});
