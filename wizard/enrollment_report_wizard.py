from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AcademyEnrollmentReportWizard(models.TransientModel):
    _name = 'academy.enrollment.report.wizard'
    _description = 'Enrollment Report Wizard (date filter)'

    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)

    student_ids = fields.Many2many('res.partner', string='Students')

    course_id = fields.Many2one('academy.course', string='Course', required=True, readonly=True)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_to < wizard.date_from:
                raise ValidationError(_("End Date cannot be earlier than Start Date."))

    def generate_report(self):
        self.ensure_one()

        domain = [
            ('course_id', '=', self.course_id.id),
            ('enrollment_date', '>=', self.date_from),
            ('enrollment_date', '<=', self.date_to),
        ]
        if self.student_ids:
            domain.append(('student_id', 'in', self.student_ids.ids))

        enrollments = self.env['academy.enrollment'].search(domain, order='enrollment_date asc')

        data = {
            'course_name': self.course_id.display_name,
            'date_from': self.date_from.strftime('%Y-%m-%d'),
            'date_to': self.date_to.strftime('%Y-%m-%d'),
            'selected_students': ', '.join(self.student_ids.mapped('name')) if self.student_ids else 'All',
            'results_count': len(enrollments),
            'enrollment_ids': enrollments.ids, # Pass the IDs to the report
        }

        return self.env.ref('academy_lab.report_enrollment_by_filters').report_action(enrollments.ids, data=data)
