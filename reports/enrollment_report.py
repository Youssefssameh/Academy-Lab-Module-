from odoo import models

class EnrollmentReport(models.AbstractModel):
    _name = 'report.academy_lab.enrollment_report_template'
    _description = 'Enrollment Report'

    def _get_report_values(self, docids, data=None):
        if not data:
            data = {}
        enrollment_ids = data.get('enrollment_ids', docids)
        enrollments = self.env['academy.enrollment'].browse(enrollment_ids)
        
        return {
            'doc_ids': enrollment_ids,
            'doc_model': 'academy.enrollment',
            'docs': enrollments,
            'data': data,
        }
