from odoo import models, fields , api
from odoo.exceptions import ValidationError

class AcademyCourse(models.Model):
    _name='academy.course'
    _description='Academy Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']  
    
    name=fields.Char(string='Title', required=True,tracking=True)
    code=fields.Char(string='Code', required=True,index=True,tracking=True)
    description=fields.Text(string='Description')
    instructor_id=fields.Many2one('res.partner', string='Instructor',tracking=True)
    category_id=fields.Many2one('academy.course.category', string='Category',tracking=True)
    duration_hours=fields.Float(string='Duration (hours)',tracking=True)
    max_students=fields.Integer(string='Max Students',tracking=True , default=20)
    
    state=fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('in_progress', 'In Progress'),
        ('done' , 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    start_date=fields.Date(string='Start Date',tracking=True)
    end_date=fields.Date(string='End Date',tracking=True)

    enrollment_ids=fields.One2many('academy.enrollment', 'course_id', string='Enrollments')

    enrolled_count=fields.Integer(string='Enrolled Students', compute='_compute_enrolled_student_count', store=True)
    available_seats=fields.Integer(string='Available Seats', compute='_compute_available_seats', store=True)
    is_full=fields.Boolean(string='Is Full', compute='_compute_is_full', store=True)

    instructor_name=fields.Char(string='Instructor Name', related='instructor_id.name', store=True) 
    product_ids= fields.One2many('product.template', inverse_name='course_id',string='Products',readonly=True)

    _sql_constraints = [
        ('code_unique', 'unique("code")', 'Course code must be unique.')
    ]

    @api.depends('enrollment_ids.state')
    def _compute_enrolled_student_count(self):
        for course in self:
            course.enrolled_count = len(course.enrollment_ids.filtered(lambda e: e.state == 'confirmed'))
    
    @api.depends('max_students', 'enrolled_count')
    def _compute_available_seats(self):
        for course in self:
            course.available_seats = course.max_students - course.enrolled_count
    
    @api.depends('available_seats')
    def _compute_is_full(self):
        for course in self:
            course.is_full = course.available_seats <= 0


    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for course in self:
            if course.end_date and course.start_date and course.end_date < course.start_date:
                raise ValidationError("End Date cannot be earlier than Start Date.")

    @api.constrains('max_students')
    def _check_max_students(self):
        for course in self:
            if course.max_students <= 0:
                raise ValidationError("Max Students must be a positive integer.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code'):
                vals['code'] = vals['code'].upper()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super().write(vals)
    
    def action_publish(self):
        self.state = 'published'
    
    def action_start(self):
        self.state = 'in_progress'

    def action_complete(self):
        self.state = 'done'
    
    def action_cancel(self):
        self.state = 'cancelled'

