from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()

        Enrollment = self.env['academy.enrollment']

        for order in self:
            student = order.partner_id

            for line in order.order_line:
                product = line.product_id
                if not product:
                    continue

                course = product.product_tmpl_id.course_id
                if not course:
                    continue

                exists = Enrollment.search([
                    ('student_id', '=', student.id),
                    ('course_id', '=', course.id),
                ], limit=1)

                if not exists:
                    Enrollment.create({
                        'student_id': student.id,
                        'course_id': course.id,
                        'state': 'draft',
                    })

        return res
