from odoo import http
from odoo.http import request


class AttendanceController(http.Controller):
    @http.route('/attendance/check', type='json', auth='user')
    def check_attendance(self, **kwargs):
        employee = request.env.user.employee_id
        if not employee:
            return {'error': 'No employee associated with this user'}

        remote_ip = request.httprequest.remote_addr
        device = request.env['attendance.device'].search([
            ('ip_address', '=', remote_ip),
            ('active', '=', True)
        ], limit=1)

        if not device:
            return {'error': 'This IP address is not allowed for attendance'}

        if employee not in device.employee_ids:
            return {'error': 'You are not allowed to check in/out from this device'}

        attendance = employee.current_attendance_id
        if attendance:
            attendance.write({
                'check_out': fields.Datetime.now(),
                'check_out_device_id': device.id
            })
            return {'status': 'checked_out', 'attendance_id': attendance.id}
        else:
            attendance = request.env['hr.attendance'].create({
                'employee_id': employee.id,
                'check_in': fields.Datetime.now(),
                'device_id': device.id
            })
            return {'status': 'checked_in', 'attendance_id': attendance.id}