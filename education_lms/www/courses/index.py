from education_lms.education_lms.utils import get_enrolled_courses, get_live_courses
import frappe
from frappe import _


def get_context(context):
	context.no_cache = 1
	context.enrolled_courses = get_enrolled_courses()
	context.show_live_courses = frappe.db.get_single_value("LMS Settings", 'show_live_courses')
	if context.show_live_courses:
		context.live_courses = get_live_courses(context.enrolled_courses)

	context.metatags = {
		"title": _("Course List"),
		"image": frappe.db.get_single_value("Website Settings", "banner_image"),
		"description": "This page lists all the courses for student",
		"keywords": "All Courses, Courses, Learn",
	}
	return context
