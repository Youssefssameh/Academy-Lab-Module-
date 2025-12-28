from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()

        Enrollment = self.env['academy.enrollment']

        for move in self:
            if move.move_type != 'out_invoice':
                continue

            student = move.partner_id

            for line in move.invoice_line_ids:
                product = line.product_id
                if not product:
                    continue

                course = product.product_tmpl_id.course_id
                if not course:
                    continue

                enrollment = Enrollment.search([
                    ('student_id', '=', student.id),
                    ('course_id', '=', course.id),
                ], limit=1)

                if enrollment:
                    enrollment.write({
                        'state': 'confirmed',
                        'invoice_id': move.id,
                    })

        return res
