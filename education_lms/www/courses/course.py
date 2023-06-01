
import frappe
from education_lms.education_lms.utils import redirect_to_courses_list, get_course_progress

def get_context(context):
    context.no_cache = 1
    print("sssssssssssssssssssss")
    try:
        course_name = frappe.form_dict["course-id"]
        set_course_context(context, course_name)
    except KeyError:
        redirect_to_courses_list()



def set_course_context(context, course_name):
    course = frappe.db.get_value(
        "Course",
        course_name,
        [
            "name",
            "course_name",
            "hero_image",
            "description",
            "published",
            "course_points",
            "resource_link"
        ],
        as_dict=True,
    )


    if course is None:
        redirect_to_courses_list()


    context.course = course
    progress = get_course_progress(course.name, frappe.session.user)
    print(progress)
    context.progress = progress

    context.metatags = {
        "title": course.course_name,
        "image": course.hero_image,
        "description": course.description,
        "keywords": course.course_name,
        "og:type": "website",
    }

