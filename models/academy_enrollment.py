from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AcademyEnrollment(models.Model):
    _name = 'academy.enrollment'
    _description = 'Academy Enrollment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id=fields.Many2one('res.partner',string='Student', required=True, tracking=True)
    course_id=fields.Many2one('academy.course', string='Course', required=True, tracking=True)
    enrollment_date=fields.Date(string='Enrollment Date', default=fields.Date.context_today, tracking=True)
    state=fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ], string='Status', default='draft', tracking=True)
    grade=fields.Float(string='Grade')
    attendance_percentage=fields.Float(string='Attendance Percentage')
    notes=fields.Text(string='Notes')
    student_name=fields.Char(string='Student Name', related='student_id.name', store=True)
    course_name=fields.Char(string='Course Name', related='course_id.name', store=True)
    passed=fields.Boolean(string='Passed', compute='_compute_passed', store=True)
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    _sql_constraints = [
        ('unique_enrollment', 'unique(student_id, course_id)', 'A student can only be enrolled once in a course.')
    ]
    
    @api.depends('grade', 'attendance_percentage')
    def _compute_passed(self):
        for rec in self:
            if rec.grade is False or rec.attendance_percentage is False:
                rec.passed = False
            else:
                rec.passed = (rec.grade >= 60) and (rec.attendance_percentage >= 75)

    @api.constrains('grade', 'attendance_percentage')
    def _check_grade_attendance_range(self):
        for rec in self:
            if rec.grade is not False and (rec.grade < 0 or rec.grade > 100):
                raise ValidationError('Grade must be between 0 and 100.')

            if rec.attendance_percentage is not False and (rec.attendance_percentage < 0 or rec.attendance_percentage > 100):
                raise ValidationError('Attendance percentage must be between 0 and 100.')

    def action_confirm(self):
        for enrollment in self:
            if enrollment.course_id.available_seats <= 0:
                raise ValidationError('Cannot confirm enrollment: Course is full.')
            enrollment.state = 'confirmed'

    def action_cancel(self):
        for enrollment in self:
            enrollment.state = 'cancelled'
    def action_complete(self):
        for enrollment in self:
            enrollment.state = 'completed'

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
            'target': 'new',
        }

