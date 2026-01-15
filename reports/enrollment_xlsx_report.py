
from odoo import models

class EnrollmentXlsxReport(models.AbstractModel):
    _name = 'report.academy_lab.enrollment_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Enrollment XLSX Report'

    def generate_xlsx_report(self, workbook, data, enrollments):
        sheet = workbook.add_worksheet('Enrollments')

        header_fmt = workbook.add_format({'bold': True})
        date_fmt = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        percent_fmt = workbook.add_format({'num_format': '0.00'})

        # adujsting column width
        sheet.set_column(0, 0, 25)  # Student
        sheet.set_column(1, 1, 25)  # Course
        sheet.set_column(2, 2, 18)  # Enrollment Date
        sheet.set_column(3, 3, 14)  # Status
        sheet.set_column(4, 4, 10)  # Grade
        sheet.set_column(5, 5, 16)  # Attendance %
        sheet.set_column(6, 6, 10)  # Passed
        sheet.set_column(7, 7, 20)  # Invoice

        headers = [
            'Student', 'Course', 'Enrollment Date', 'Status',
            'Grade', 'Attendance %', 'Passed', 'Invoice'
        ]

        # Header row
        for col, title in enumerate(headers):
            sheet.write(0, col, title, header_fmt)

        # Data rows
        row = 1
        for rec in enrollments:
            sheet.write(row, 0, rec.student_id.name or '')
            sheet.write(row, 1, rec.course_id.name or '')

            # Date 
            if rec.enrollment_date:
                sheet.write(row, 2, str(rec.enrollment_date), date_fmt)
            else:
                sheet.write(row, 2, '')

            # Status label
            status_label = dict(rec._fields['state'].selection).get(rec.state, rec.state or '')
            sheet.write(row, 3, status_label)

            sheet.write_number(row, 4, rec.grade or 0)
            sheet.write_number(row, 5, rec.attendance_percentage or 0, percent_fmt)

            sheet.write(row, 6, 'Yes' if rec.passed else 'No')

            # invoice name/number (display_name)
            sheet.write(row, 7, rec.invoice_id.display_name or '')

            row += 1

        sheet.freeze_panes(1, 0)  # header fix 
