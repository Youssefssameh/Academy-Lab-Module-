from odoo import models
from odoo.exceptions import AccessError

class StudentTranscriptReport(models.AbstractModel):
    _name = 'report.academy_lab.student_transcript_template'
    _description = 'Student Transcript Report'

    def _get_report_values(self, docids, data=None):
        students = self.env['res.partner'].browse(docids)
        
        # Access Control: Student يشوف transcript بتاعه بس
        if self.env.user.has_group('academy_lab.academy_group_student'):
            for student in students:
                if student.id != self.env.user.partner_id.id:
                    raise AccessError(
                        "You are not allowed to print transcripts for other students. "
                        "You can only print your own transcript."
                    )
        
        # الحسابات
        result = []
        for student in students:
            # جيب كل enrollments للطالب ده
            enrollments = self.env['academy.enrollment'].search([
                ('student_id', '=', student.id)
            ], order='enrollment_date desc')
            
            # Statistics
            total_courses = len(enrollments)
            grades = [e.grade for e in enrollments if e.grade]
            avg_grade = sum(grades) / len(grades) if grades else 0.0
            
            # Top 3 courses (أعلى grades)
            top_3 = enrollments.filtered(lambda e: e.grade).sorted(
                key=lambda e: e.grade, reverse=True
            )[:3]
            
            result.append({
                'student': student,
                'enrollments': enrollments,
                'total_courses': total_courses,
                'avg_grade': round(avg_grade, 2),
                'top_3': top_3,
            })
        
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': students,
            'data': data or {},
            'students_data': result,
        }
