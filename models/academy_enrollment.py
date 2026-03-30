from odoo import models, fields, api
from odoo.exceptions import ValidationError , UserError

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
    

    ui_hint = fields.Char(
        string="UI Hint",
        compute="_compute_ui_hint",
        store=False,
        readonly=True,
    )

    reservation_deadline = fields.Datetime(string="Reservation Deadline",tracking=True)
    is_reservation_active = fields.Boolean(string="Is Reservation Active", compute="_compute_reservation_flags",store=False)
    is_reservation_expired = fields.Boolean(string="Is Reservation Expired", compute="_compute_reservation_flags",store=False)

    cancel_reason = fields.Selection([
        ('expired', 'Expired Reservation'),
        ('manual', 'Manual Cancel'),
        ('other', 'Other'),
    ], string="Cancel Reason", tracking=True)

    @api.depends('state', 'reservation_deadline')
    def _compute_reservation_flags(self):
        now = fields.Datetime.now()
        for rec in self:
            # Active: still draft and deadline not passed
            rec.is_reservation_active = bool(
                rec.state == 'draft'
                and rec.reservation_deadline
                and rec.reservation_deadline > now
            )
            # Expired: either (draft & passed deadline) 
            rec.is_reservation_expired = bool(
                (rec.state == 'draft' and rec.reservation_deadline and rec.reservation_deadline <= now)
            )

    def _is_reservation_valid(self):
        """True only when draft reservation is still within its deadline."""
        self.ensure_one()
        if self.state != 'draft':
            return False
        if not self.reservation_deadline:
            return False
        return self.reservation_deadline > fields.Datetime.now()

    # ✅ Cron target
    @api.model
    def _cron_expire_reservations(self):
        now = fields.Datetime.now()
        expired = self.search([
            ('state', '=', 'draft'),
            ('reservation_deadline', '!=', False),
            ('reservation_deadline', '<=', now),
        ])
        if expired:
            expired.write({
                'state': 'cancelled',
                'cancel_reason': 'expired',
            })


    @api.depends('grade', 'attendance_percentage')
    def _compute_ui_hint(self):
        for rec in self:
            if rec.grade in (False, None) or rec.attendance_percentage in (False, None):
                rec.ui_hint = "Hint will appear here based on grade/attendance"
            elif rec.grade < 60:
                rec.ui_hint = "⚠ Grade is below 60"
            elif rec.attendance_percentage < 75:
                rec.ui_hint = "⚠ Attendance is below 75%"
            else:
                rec.ui_hint = "✅ Looks good"


    # @api.onchange('grade', 'attendance_percentage')
    # def _onchange_grade_attendance_ui(self):
    #     """
    #     Provides UI hints based on grade and attendance percentage.

    #     - If either grade or attendance is missing, prompts user to enter both.
    #     - If grade < 60, warns that grade is below passing threshold.
    #     - If attendance < 75%, warns that attendance is below required percentage.
    #     - If both are satisfactory, indicates that the student will pass if saved.
    #     - If values are out of range (not between 0 and 100), shows a warning pop-up.

    #     """
    #     for rec in self:
    #         g = rec.grade
    #         a = rec.attendance_percentage

    #         # main hints
    #         if g < 60:
    #             rec.ui_hint = "⚠ Grade is below 60"
    #         elif a < 75:
    #             rec.ui_hint = "⚠ Attendance is below 75%"
    #         else:
    #             rec.ui_hint = "✅ Looks good: will PASS if saved"

    #         # warning pop-up
    #         if (g < 0 or g > 100) or (a < 0 or a > 100):
    #             return {
    #                 'warning': {
    #                     'title': 'Invalid Range',
    #                     'message': 'Grade/Attendance should be between 0 and 100 (saving will be blocked).'
    #                 }
    #             }

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
            #block confirm if expired reservation
            if enrollment.state == 'draft' and enrollment.reservation_deadline and enrollment.reservation_deadline <= fields.Datetime.now():
                raise UserError("This reservation has expired. Please create a new reservation.")
            #capacity check 
            if enrollment.course_id.available_seats <= 0:
                raise ValidationError('Cannot confirm enrollment: Course is full.')
            enrollment.state = 'confirmed'

    def action_cancel(self):
        for enrollment in self:
            if enrollment.state != 'cancelled':
                enrollment.cancel_reason = enrollment.cancel_reason or 'manual'
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

