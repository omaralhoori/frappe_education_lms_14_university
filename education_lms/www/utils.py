import frappe

from education_lms.education_lms.utils import get_lesson_url, get_lessons, get_course_progress


def get_common_context(context):
	context.no_cache = 1

	course = frappe.db.get_value(
		"Course",
		frappe.form_dict["course"],
		["name", "course_name", "hero_image"],
		as_dict=True,
	)
	if not course:
		context.template = "www/404.html"
		return
	context.course = course
	context.lessons = get_lessons(course.name)
	membership = get_course_progress(course.name, frappe.session.user)
	context.membership = membership



def redirect_to_lesson(course, lesson_type, lesson):
	frappe.local.flags.redirect_location = (
		get_lesson_url(course.name, lesson_type, lesson)
	)
	raise frappe.Redirect


