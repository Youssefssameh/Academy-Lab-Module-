# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound

_logger = logging.getLogger(__name__)


class AcademyEnrollmentController(http.Controller):

    @http.route('/academy/ping', type='http', auth='public', website=True)
    def academy_ping(self, **kw):
        return "PING OK ✅"
    
    @http.route(
        [
            '/academy/course/<int:course_id>/enrollments', #http://localhost:4062/academy/course/<course_id>/enrollments
            '/odoo/academy/course/<int:course_id>/enrollments',
        ],
        type='http',
        auth='user',
        website=True
    )
    def course_enrollments_page(self, course_id, **kw):

        _logger.warning("✅ AcademyEnrollmentController LOADED")

        Course = request.env['academy.course'].sudo()
        Enrollment = request.env['academy.enrollment'].sudo()

        course = Course.browse(course_id)
        if not course.exists():
            raise NotFound()

        domain = [('course_id', '=', course.id)]

        values = {
            'course': course,
            'total': Enrollment.search_count(domain),
            'draft_count': Enrollment.search_count(domain + [('state', '=', 'draft')]),
            'confirmed_count': Enrollment.search_count(domain + [('state', '=', 'confirmed')]),
            'cancelled_count': Enrollment.search_count(domain + [('state', '=', 'cancelled')]),
            'completed_count': Enrollment.search_count(domain + [('state', '=', 'completed')]),
            'enrollments': Enrollment.search(domain, order='create_date desc', limit=10),
        }

        return request.render(
            'academy_lab.course_enrollments_dashboard',
            values
        )
