from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'

    allowed_ip_ids = fields.Many2many('attendance.device', string='Allowed Devices')
    current_attendance_id = fields.Many2one('hr.attendance', compute='_compute_current_attendance')
    break_ids = fields.One2many('attendance.break', 'employee_id', string='Breaks')

    def _compute_current_attendance(self):
        for emp in self:
            emp.current_attendance_id = self.env['hr.attendance'].search([
                ('employee_id', '=', emp.id),
                ('check_out', '=', False)
            ], limit=1)
    # 1. First declare the One2many relationship
    break_ids = fields.One2many(
        'attendance.break',  # Related model
        'employee_id',  # Inverse field name in break model
        string='Employee Breaks'
    )

    # 2. Then declare computed fields
    current_break_start = fields.Datetime(
        compute='_compute_current_break',
        string='Current Break Start',
        store=False  # Don't store in database
    )
    current_break_end = fields.Datetime(
        compute='_compute_current_break',
        string='Current Break End',
        store=False
    )
    current_break_duration = fields.Float(
        compute='_compute_current_break',
        string='Current Break Duration',
        store=False
    )

    # 3. Correct compute method
    @api.depends('break_ids.start_time', 'break_ids.end_time')
    def _compute_current_break(self):
        """Compute current break details from related break records"""
        for employee in self:
            # Find the most recent active break (started but not ended)
            active_break = employee.break_ids.filtered(
                lambda b: b.start_time and not b.end_time
            )[:1]

            employee.update({
                'current_break_start': active_break.start_time if active_break else False,
                'current_break_end': active_break.end_time if active_break else False,
                'current_break_duration': active_break.duration if active_break else 0.0,
            })