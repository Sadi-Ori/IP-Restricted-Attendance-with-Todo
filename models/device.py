from odoo import models, fields, api


class AttendanceDevice(models.Model):
    _name = 'attendance.device'
    _description = 'Attendance Device'

    name = fields.Char(string='Device Name', required=True)
    ip_address = fields.Char(string='IP Address', required=True)
    location = fields.Char(string='Location', required=True)
    active = fields.Boolean(string='Active', default=True)
    employee_ids = fields.Many2many(
        'hr.employee',
        string='Allowed Employees'
    )

    _sql_constraints = [
        ('ip_address_unique', 'unique(ip_address)', 'IP Address must be unique!'),
    ]