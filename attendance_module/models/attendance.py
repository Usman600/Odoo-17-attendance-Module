from odoo import models, fields, api
from datetime import datetime


class AttendanceRecord(models.Model):
    _name = 'attendance.record'
    _description = 'Employee Attendance'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    check_in = fields.Datetime(string='Arrival Time', required=False)
    check_out = fields.Datetime(string='Departure Time', required=False)
    worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours', store=True)
    status = fields.Selection([('present', 'Present'), ('late', 'Late'), ('absent', 'Absent')])

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for record in self:
            if record.check_in and record.check_out:
                worked_duration = record.check_out - record.check_in
                record.worked_hours = worked_duration.total_seconds() / 3600.0
            else:
                record.worked_hours = 0.0

    def register_attendance(self):
        for record in self:

            if not record.check_in:

                record.check_in = fields.Datetime.now()
                record.status = 'present'
            elif not record.check_out:

                record.check_out = fields.Datetime.now()
                record.status = 'present'

            record._compute_worked_hours()

    @api.onchange('check_in', 'check_out')
    def _onchange_status(self):
        for record in self:

            if record.check_in:
                record.status = 'present'
            elif not record.check_in and not record.check_out:
                record.status = 'absent'
            else:
                record.status = 'absent'
