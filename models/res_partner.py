from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student=fields.Boolean(string='Is Student', default=False)
    is_instructor=fields.Boolean(string='Is Instructor', default=False)
    student_enrollment_ids=fields.One2many('academy.enrollment', 'student_id', string='Student Enrollments')
    instructor_course_ids=fields.One2many('academy.course', 'instructor_id', string='Instructor Courses')
    total_courses_enrolled=fields.Integer(string='Total Courses Enrolled', compute='_compute_total_courses_enrolled')
    total_courses_teaching=fields.Integer(string='Total Courses Taught', compute='_compute_total_courses_teaching')

    @api.depends('student_enrollment_ids')
    def _compute_total_courses_enrolled(self):
        for partner in self:
            partner.total_courses_enrolled = len(partner.student_enrollment_ids)
    
    @api.depends('instructor_course_ids')
    def _compute_total_courses_teaching(self):
        for partner in self:
            partner.total_courses_teaching = len(partner.instructor_course_ids)