odoo.define('ip_restricted_attendance.AttendanceDashboard', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');
    var session = require('web.session');
    var QWeb = core.qweb;

    var AttendanceDashboard = Widget.extend({
        template: 'AttendanceDashboard',
        events: {
            'click .o_check_in_out': '_onCheckInOut',
            'click .o_start_break': '_onStartBreak',
            'click .o_end_break': '_onEndBreak',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.employee_id = options.employee_id || null;
            this.current_attendance = options.current_attendance || null;
            this.current_break = null;
        },

        willStart: function () {
            var self = this;
            return $.when(
                this._super.apply(this, arguments),
                this._loadData()
            );
        },

        _loadData: function () {
            var self = this;
            return this._rpc({
                model: 'hr.employee',
                method: 'get_attendance_dashboard_data',
                args: [[this.employee_id]],
            }).then(function (result) {
                self.data = result;
            });
        },

        _onCheckInOut: function (ev) {
            ev.preventDefault();
            var self = this;
            this._rpc({
                route: '/attendance/check',
                params: {},
            }).then(function (result) {
                if (result.error) {
                    self.do_warn(result.error);
                } else {
                    self.reload();
                }
            });
        },

        _onStartBreak: function (ev) {
            ev.preventDefault();
            var self = this;
            this._rpc({
                model: 'attendance.break',
                method: 'create',
                args: [{
                    'name': 'Break',
                    'employee_id': this.employee_id,
                }],
            }).then(function () {
                self.reload();
            });
        },

        _onEndBreak: function (ev) {
            ev.preventDefault();
            var self = this;
            this._rpc({
                model: 'attendance.break',
                method: 'action_end_break',
                args: [[this.current_break]],
            }).then(function () {
                self.reload();
            });
        },

        reload: function () {
            var self = this;
            return this._loadData().then(function () {
                self.$el.html(QWeb.render('AttendanceDashboard', {
                    widget: self,
                    data: self.data,
                }));
            });
        },
    });

    core.action_registry.add('attendance_dashboard', AttendanceDashboard);

    return {
        AttendanceDashboard: AttendanceDashboard,
    };
});