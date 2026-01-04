from odoo import models
from odoo.exceptions import AccessError

class StudentTranscriptReport(models.AbstractModel):
    _name = 'report.academy_lab.student_transcript_template'
    _description = 'Student Transcript Report'

    def _get_report_values(self, docids, data=None):
        students = self.env['res.partner'].browse(docids)

        user = self.env.user
        is_student = user.has_group('academy_lab.academy_group_student')
        is_instructor = user.has_group('academy_lab.academy_group_instructor')
        is_manager = user.has_group('academy_lab.academy_group_manager')


        if is_student and not (is_instructor or is_manager):
            students = students.filtered(lambda s: s.id == user.partner_id.id)
            if not students:
                raise AccessError(
                    "You can only print your own transcript."
                )
        
        result = []
        for student in students:
            
            enrollments = self.env['academy.enrollment'].search([
                ('student_id', '=', student.id)
            ], order='enrollment_date desc')
            
            # Statistics
            total_courses = len(enrollments)
            grades = [e.grade for e in enrollments if e.grade]
            avg_grade = sum(grades) / len(grades) if grades else 0.0
            
            
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
