import frappe
from frappe import _
from frappe.utils import cstr, flt

from education_lms.education_lms.utils import get_lesson_url
from education_lms.www.utils import get_common_context, redirect_to_lesson


def get_context(context):
	get_common_context(context)

	lesson_type = frappe.form_dict.get("lesson-type")
	lesson = frappe.form_dict.get("lesson")
	course = frappe.form_dict.get("course")
	
	# context.chapter = frappe.db.get_value(
	# 	"Chapter Reference", {"idx": chapter_index, "parent": context.course.name}, "chapter"
	# )


	context.lesson = get_current_lesson_details(lesson_type, lesson, context)
	context.show_lesson = (
		context.membership.course_enabled
	)

	if not context.lesson:
		context.lesson = frappe._dict()


	neighbours = get_neighbours(context.lesson.idx, context.lessons)
	context.next_url = get_url(neighbours["next"], context.course)
	context.prev_url = get_url(neighbours["prev"], context.course)

	meta_info = (
		context.lesson.title + " - " + context.course.course_name
		if context.lesson.title
		else "New Lesson"
	)
	context.metatags = {
		"title": meta_info,
		"keywords": meta_info,
		"description": meta_info,
	}

	context.page_context = {
		"course": context.course.name,
		"lesson": context.lesson.name if context.lesson.name else "New Lesson",
		"is_member": context.membership.course_enabled,
	}


def get_current_lesson_details(lesson_type, lesson, context):
	details_list = list(filter(lambda x: (x.content_type == lesson_type and x.content == lesson), context.lessons))

	if not len(details_list):
			redirect_to_lesson(context.course, lesson_type, lesson)

	lesson_info = details_list[0]
	#lesson_info.body = lesson_info.body.replace('"', "'")
	return lesson_info


def get_url(lesson, course):
	if not lesson: return None
	return (
		get_lesson_url(course.name, lesson.content_type, lesson.content)
	)



def get_neighbours(current, lessons):
	current = flt(current)
	numbers = sorted(flt(lesson.idx) for lesson in lessons)
	index = numbers.index(current)
	prev_lesson,next_lesson = None, None
	for lesson in lessons:
		if index - 1 >= 0:
			if flt(lesson.idx) == numbers[index - 1]:
				prev_lesson = lesson
		if index + 1 < len(numbers):
			if flt(lesson.idx) == numbers[index + 1] :
				next_lesson = lesson
	return {
		"prev": prev_lesson,
		"next": next_lesson,
	}
