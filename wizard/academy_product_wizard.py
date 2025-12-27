from odoo import models, fields
from odoo.exceptions import UserError

class AcademyProductWizard(models.TransientModel):
    _name='academy.product.wizard'
    _description='Academy Product Wizard'

    name = fields.Char(string='Product Name', required=True)
    price = fields.Float(string='Product Price', required=True)

    def create_product(self):
        self.ensure_one()

        active_id = self.env.context.get('active_id')
        if not active_id:
            raise UserError("no active course found. Please open this wizard from a Course")

        course = self.env['academy.course'].browse(active_id)
        if not course.exists():
            raise UserError("Course not found")

        if course.product_id:
            raise UserError("This course already has a product ")

        product_vals = {
            'name': self.name,
            'list_price': self.price,
            'type': 'service',
            'course_id': course.id,  
        }
        product = self.env['product.product'].create(product_vals)

        course.write({'product_id': product.id})

        return {'type': 'ir.actions.act_window_close'}