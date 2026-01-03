from odoo import models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        Enrollment = self.env['academy.enrollment']

        for order in self:
            student = order.partner_id
            courses = order.order_line.mapped('product_id.product_tmpl_id.course_id')
            courses = courses.filtered(lambda c: c)
            if not courses:
                continue
            existing = Enrollment.search([
                ('student_id', '=', student.id),
                ('course_id', 'in', courses.ids),
            ])
            if existing:
                dup_courses = existing.mapped('course_id')
                dup_names = "\n- " + "\n- ".join(dup_courses.mapped('name'))
                raise UserError(
                    "Cannot confirm this Sales Order because the customer is already enrolled in:\n"
                    "%(courses)s\n\n"
                    "Student: %(student)s"
                ) % {
                    'courses': dup_names,
                    'student': student.name,
                }
        
        res = super().action_confirm()
        for order in self:
            student = order.partner_id
            courses = order.order_line.mapped('product_id.product_tmpl_id.course_id').filtered(lambda c: c)
            existing_courses = Enrollment.search([
                ('student_id', '=', student.id),
                ('course_id', 'in', courses.ids),
            ]).mapped('course_id')
            existing_course_ids = set(existing_courses.ids)
            for course in courses:
                if course.id in existing_course_ids:
                    continue
                # will be done in future
                # if course.available_seats <= 0:
                #     raise UserError(
                #         "Cannot enroll student %(student)s in course %(course)s because there are no seats available. \n Please remove the course %(course)s from the order."
                #     ) % {
                #         'student': student.name,
                #         'course': course.name,
                #     }
                Enrollment.create({
                    'student_id': student.id,
                    'course_id': course.id,
                    'state': 'draft',
                })

        return res
