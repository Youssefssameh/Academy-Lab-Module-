from odoo import models, fields, api 


class AcademyCourseCategory(models.Model):
    _name = 'academy.course.category'
    _description = 'Academy Course Category'
    
    name=fields.Char(string='Name', required=True)
    description=fields.Text(string='Description')
    course_ids=fields.One2many('academy.course', 'category_id', string='Courses')
    course_count=fields.Integer(string='Course count',compute='_count_courses',store=True)

    @api.depends('course_ids')
    def _count_courses(self):
        for category in self:
            category.course_count = len(category.course_ids)
