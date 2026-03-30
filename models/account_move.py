from odoo import models, fields
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()

        Enrollment = self.env['academy.enrollment']
        now = fields.Datetime.now()

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
                    ('state', '=', 'draft'),
                ], limit=1)

                if not enrollment:
                    # If it was cancelled due to expiry, block posting too
                    cancelled_expired = Enrollment.search([
                        ('student_id', '=', student.id),
                        ('course_id', '=', course.id),
                        ('state', '=', 'cancelled'),
                        ('cancel_reason', '=', 'expired'),
                    ], limit=1)

                    if cancelled_expired:
                        raise UserError(
                            f"Cannot post invoice.\n"
                            f"The reservation for course '{course.name}' has expired.\n"
                            f"Please create a new reservation."
                        )

                    # No reservation at all (or cancelled manually/other): block posting
                    raise UserError(
                        f"Cannot post invoice.\n"
                        f"No active reservation found for course '{course.name}' for customer '{student.name}'.\n"
                        f"Please confirm a Sales Order to create a reservation first."
                    )

                # 1️⃣ لو reservation انتهت → نمنع
                if enrollment.reservation_deadline and enrollment.reservation_deadline <= now:
                    raise UserError(
                        f"Cannot post invoice.\n"
                        f"The reservation for course '{course.name}' has expired.\n"
                        f"Please create a new reservation."
                    )

                # 2️⃣ لو الكورس full وقت التأكيد → نمنع
                reserved_minus_this = max(course.reserved_count - 1, 0)
                seats_after_confirm = course.max_students - (course.enrolled_count + reserved_minus_this)

                if seats_after_confirm <= 0:
                    raise UserError(
                        f"Cannot confirm enrollment.\n"
                        f"The course '{course.name}' is already full."
                    )

                # 3️⃣ Confirm enrollment + link invoice
                enrollment.write({
                    'state': 'confirmed',
                    'invoice_id': move.id,
                })

        return res
