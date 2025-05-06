from odoo import models, fields, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    device_id = fields.Many2one(
        'attendance.device',
        string='Check-in Device',
        index=True  # Add this for better performance
    )
    check_out_device_id = fields.Many2one(
        'attendance.device',
        string='Check-out Device',
        index=True  # Add this for better performance
    )
    break_ids = fields.One2many(
        'attendance.break',
        'attendance_id',
        string='Breaks'
    )
    total_break_duration = fields.Float(
        string='Total Break Duration',
        compute='_compute_total_break_duration'
    )

    def _compute_total_break_duration(self):
        for attendance in self:
            total = 0.0
            for br in attendance.break_ids:
                if br.start_time and br.end_time:
                    total += (br.end_time - br.start_time).total_seconds() / 3600
            attendance.total_break_duration = total

    @api.model
    def create(self, vals):
        if 'device_id' in vals:
            device = self.env['attendance.device'].browse(vals['device_id'])
            vals['check_in_location'] = device.location
        return super().create(vals)

    def write(self, vals):
        if 'check_out_device_id' in vals:
            device = self.env['attendance.device'].browse(vals['check_out_device_id'])
            vals['check_out_location'] = device.location
        return super().write(vals)