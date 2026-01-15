
from odoo import models

# Shared formats dictionary from report_xlsx_helper
from odoo.addons.report_xlsx_helper.report.report_xlsx_format import FORMATS


class EnrollmentXlsxReport(models.AbstractModel):
    _name = "report.academy_lab.enrollment_xlsx_report"
    _inherit = "report.report_xlsx.abstract"
    _description = "Enrollment XLSX Report"

    def generate_xlsx_report(self, workbook, data, enrollments):
        """
        Entry point called by Odoo when the XLSX report is generated.
        We prepare helper formats and then generate the worksheet content.
        """
        # Initialize the predefined formats from report_xlsx_helper
        self._define_formats(workbook)

        # Create one worksheet
        ws = workbook.add_worksheet("Enrollments")

        # Get predefined formats
        title_fmt = FORMATS["format_ws_title"]
        header_fmt = FORMATS["format_left_bold"]
        date_fmt = FORMATS["format_date_left"]
        percent_fmt = FORMATS["format_percent_right"]
        num_fmt = FORMATS["format_amount_right"]

        # Title
        ws.write(0, 0, "Enrollments Report", title_fmt)

        # Column widths
        ws.set_column(0, 0, 25)  # Student
        ws.set_column(1, 1, 25)  # Course
        ws.set_column(2, 2, 18)  # Enrollment Date
        ws.set_column(3, 3, 14)  # Status
        ws.set_column(4, 4, 10)  # Grade
        ws.set_column(5, 5, 16)  # Attendance %
        ws.set_column(6, 6, 10)  # Passed
        ws.set_column(7, 7, 20)  # Invoice

        headers = [
            "Student", "Course", "Enrollment Date", "Status",
            "Grade", "Attendance %", "Passed", "Invoice"
        ]

        # Header row
        for col, title in enumerate(headers):
            ws.write(2, col, title, header_fmt)

        # Data rows
        row = 3
        for rec in enrollments:
            ws.write(row, 0, rec.student_id.name or "")
            ws.write(row, 1, rec.course_id.name or "")

            # Date as string; format keeps consistent look
            ws.write(row, 2, str(rec.enrollment_date or ""), date_fmt)

            status_label = dict(rec._fields["state"].selection).get(rec.state, rec.state or "")
            ws.write(row, 3, status_label)

            ws.write_number(row, 4, rec.grade or 0.0, num_fmt)

            # Excel percent format expects a ratio (e.g., 0.75 for 75%)
            attendance_ratio = (rec.attendance_percentage or 0.0) / 100.0
            ws.write_number(row, 5, attendance_ratio, percent_fmt)

            ws.write(row, 6, "Yes" if rec.passed else "No")
            ws.write(row, 7, rec.invoice_id.display_name or "")

            row += 1

        # Freeze the header row
        ws.freeze_panes(3, 0)
