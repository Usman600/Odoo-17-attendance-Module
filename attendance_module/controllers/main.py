from odoo import http
from odoo.http import request
from datetime import datetime

class AttendanceController(http.Controller):

    @http.route('/attendance/attendance_form', type='http', auth='user')
    def attendance_form(self):

        user = request.env.user
        attendance_obj = request.env['attendance.record']


        attendance_record = attendance_obj.search([
            ('employee_id', '=', user.employee_id.id),
            ('check_in', '!=', False),
            ('check_out', '=', False)
        ], limit=1)

        check_in = False
        if attendance_record:
            check_in = True

        return request.render('attendance_module.attendance_checkin_checkout', {
            'status': 'ready',
            'message': 'Please check in or check out',
            'check_in': check_in,  # Pass the check-in status
            'heading': 'Employee Attendance',
        })

    @http.route('/attendance/check_in', type='http', auth='user')
    def check_in(self):
        user = request.env.user
        attendance_obj = request.env['attendance.record']
        check_in_time = datetime.now()
        attendance_obj.create({
            'employee_id': user.employee_id.id,
            'check_in': check_in_time,
            'status': 'present',
        })

        return request.render('attendance_module.attendance_checkin_checkout', {
            'status': 'success',
            'message': 'Please Check Out',
            'check_in': True,
            'heading': 'Employee Attendance',
        })

    @http.route('/attendance/check_out', type='http', auth='user')
    def check_out(self):
        user = request.env.user

        attendance_obj = request.env['attendance.record']
        check_out_time = datetime.now()
        attendance_record = attendance_obj.search([
            ('employee_id', '=', user.employee_id.id),
            ('check_in', '!=', False),
            ('check_out', '=', False)
        ], limit=1)

        if attendance_record:
            attendance_record.write({'check_out': check_out_time})


        return request.render('attendance_module.attendance_checkin_checkout', {
            'status': 'success',
            'message': 'Please Check In',
            'check_in': False,
            'heading': 'Employee Attendance',
        })
