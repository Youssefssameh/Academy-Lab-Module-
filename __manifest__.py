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

        'wizard/academy_product_wizard_view.xml',
        'wizard/enrollment_report_wizard_view.xml',
        # Reports (must be loaded before views that reference them by xmlid)
        'reports/report_actions.xml',
        'reports/report_templates.xml',
        
        # Views
        'views/academy_actions.xml',
        'views/academy_course_views.xml',
        'views/academy_category_views.xml',
        'views/academy_enrollment_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_view.xml',

        # Menus last
        'views/academy_menus.xml',

    ],
    'assets': {
        'web.report_assets_common': ['academy_lab/static/src/css/font.css']
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
