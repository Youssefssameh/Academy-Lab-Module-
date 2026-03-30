from odoo import models,fields
from odoo.exceptions import UserError
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        Enrollment = self.env['academy.enrollment']

        # 1) Pre-check: prevent confirming SO if any course is full
        for order in self:
            courses = order.order_line.mapped('product_id.product_tmpl_id.course_id').filtered(lambda c: c)
            for course in courses:
                if course.available_seats <= 0:
                    raise UserError(f"Cannot confirm this Sales Order because the course is full:\n- {course.name}")

        # 2) Duplicate check (ignore cancelled so user can re-enroll after expiry/manual cancel)
        for order in self:
            student = order.partner_id
            courses = order.order_line.mapped('product_id.product_tmpl_id.course_id').filtered(lambda c: c)
            if not courses:
                continue

            existing = Enrollment.search([
                ('student_id', '=', student.id),
                ('course_id', 'in', courses.ids),
                ('state', '!=', 'cancelled'),
            ])
            if existing:
                dup_courses = existing.mapped('course_id')
                dup_names = "\n- " + "\n- ".join(dup_courses.mapped('name'))
                raise UserError(
                    "Cannot confirm this Sales Order because the customer is already enrolled (or has an active reservation) in:\n"
                    "%(courses)s\n\n"
                    "Student: %(student)s"
                ) % {
                    'courses': dup_names,
                    'student': student.name,
                }

        # 3) Confirm SO normally
        res = super().action_confirm()

        # 4) Create enrollments as draft reservations with 24h deadline
        deadline = fields.Datetime.now() + timedelta(hours=24)

        for order in self:
            student = order.partner_id
            courses = order.order_line.mapped('product_id.product_tmpl_id.course_id').filtered(lambda c: c)

            existing_courses = Enrollment.search([
                ('student_id', '=', student.id),
                ('course_id', 'in', courses.ids),
                ('state', '!=', 'cancelled'),
            ]).mapped('course_id')
            existing_course_ids = set(existing_courses.ids)

            for course in courses:
                if course.id in existing_course_ids:
                    continue
                
                Enrollment.create({
                    'student_id': student.id,
                    'course_id': course.id,
                    'state': 'draft',
                    'reservation_deadline': deadline,
                })

        return res
