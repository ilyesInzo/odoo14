var department_data = {}
var viewDepartmentfunction = {}
odoo.define("magenest_org_chart.org_chart_department_v2", function (require) {
    "use strict";
    var tags = {};
    var core = require('web.core');
    var ajax = require('web.ajax');
    var AbstractAction = require('web.AbstractAction');
    var QWeb = core.qweb;
    var OrgChartDepartment = AbstractAction.extend({
        template: "magenest_org_chart.get_org_chart_department_template",
        jsLibs: [
            '/magenest_org_chart/static/js/jquery.orgchart.js'
        ],
        init: function (parent, context) {
            this._super(parent, context);
            var self = this;
            if (context.tag == 'org_chart_department_v2') {
                self._rpc({
                    model: 'hr.department',
                    method: 'get_department_data_v2',
                }).then(function (result) {
                    department_data = result
                    viewDepartmentfunction = self.viewDepartment.bind(self)
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
            var org_chart = QWeb.render('magenest_org_chart.get_org_chart_department_template', {});
            // console.log(this)
            $(".o_control_panel").addClass("o_hidden");
            return org_chart;
        },
        reload: function () {
            window.location.href = this.href;
        },
        viewDepartment: function (object) {

            if (object.type == 'department'){
                if (object.id) {
                    var chart  = $('#chart-container')
                    chart.remove()
                    this.do_action({
                        name: 'Departments',
                        type: 'ir.actions.act_window',
                        res_model: 'hr.department',
                        res_id: object.id,
                        view_mode: 'form',
                        views: [[false, 'form']],
                    })
                }
            }
            else if (object.type == 'company')
            {
                if (object.id) {
                    var chart  = $('#chart-container')
                    chart.remove()
                    this.do_action({
                        name: 'Company',
                        type: 'ir.actions.act_window',
                        res_model: 'res.company',
                        res_id: object.id,
                        view_mode: 'form',
                        views: [[false, 'form']],
                    })
                }
            }
        }
    });

    core.action_registry.add('org_chart_department_v2', OrgChartDepartment);
    return {
        OrgChartDepartment: OrgChartDepartment
    };

});
