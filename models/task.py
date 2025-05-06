from odoo import models, fields, api
from datetime import datetime


class AttendanceTask(models.Model):
    _name = 'attendance.task'
    _description = 'Employee Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True
    )
    start_date = fields.Datetime(string='Start Date', default=fields.Datetime.now)
    end_date = fields.Datetime(string='End Date')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], string='Priority', default='medium')

    def action_start(self):
        self.write({
            'status': 'in_progress',
            'start_date': fields.Datetime.now()
        })

    def action_done(self):
        self.write({
            'status': 'done',
            'end_date': fields.Datetime.now()
        })

    def action_cancel(self):
        self.write({'status': 'cancel'})

    def action_reset(self):
        self.write({'status': 'draft'})