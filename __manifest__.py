# -*- coding: utf-8 -*-
{
    'name': "Academy Lab",
    'version': '18.0.1.0.0',
    'summary': "Training Academy Management System",
    'description': "Training academy addon: courses, categories, enrollments, and role-based security.",
    'author': "Youssef",
    'category': 'Services/Training',
    'depends': [
        'base',
        'mail',
        'contacts',
        'sale',
        'account',
    ],
    'data': [
        'security/academy_security.xml',
        'security/ir.model.access.csv',
        'security/academy_record_rules.xml',
        
        'views/academy_actions.xml',
        'views/academy_course_views.xml',
        'views/academy_category_views.xml',
        'views/academy_enrollment_views.xml',
        'views/academy_menus.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
