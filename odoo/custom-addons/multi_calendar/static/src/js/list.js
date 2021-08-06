odoo.define('list.employee.tree', function (require) {
    "use strict";
        var ListController = require('web.ListController');
        var ListView = require('web.ListView');
        var viewRegistry = require('web.view_registry');
        var core = require('web.core');
        var ListRenderer = require('web.ListRenderer');

        const config = require('web.config');

        var DocumentUploadMixin = {
            _onShowAssignEmployees: async function (event) {

                /*const result = await this._rpc({
                    model: 'calendar.assignee',
                    method: 'open_employees_wiz',
                    args: [{'test':1}
                    ],
                });*/

                this.do_action({
                type: "ir.actions.act_window",
                res_model: "assigne.employees.wizard",
                view_mode: "form",
                views: [[false, 'form']],
                context: this.initialState.context,
                target: "new"})

            },
        };

        var ExpensesListController = ListController.extend(DocumentUploadMixin, {
            buttons_template: 'ExpensesListView.buttons',
            events: _.extend({}, ListController.prototype.events, {
                'click .o_button_assigne_employees': '_onShowAssignEmployees'
            }),
        });
    
        var ExpensesListViewDashboard = ListView.extend({
            config: _.extend({}, ListView.prototype.config, {
                Renderer: ListRenderer,
                Controller: ExpensesListController,
            }),
        });
    
        var ExpensesListViewDashboardHeader = ExpensesListViewDashboard.extend({
            config: _.extend({}, ExpensesListViewDashboard.prototype.config, {
                Renderer: ListRenderer,
            })
        });

        viewRegistry.add('calender_header', ExpensesListViewDashboardHeader);

    });
    