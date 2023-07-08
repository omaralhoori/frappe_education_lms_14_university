
import frappe
from education_lms.education_lms.utils import redirect_to_courses_list, get_course_progress

def get_context(context):
    context.no_cache = 1
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

    context.progress = progress

    course_group = get_course_group(course)
    context.course_group = course_group
    context.metatags = {
        "title": course.course_name,
        "image": course.hero_image,
        "description": course.description,
        "keywords": course.course_name,
        "og:type": "website",
    }


def get_course_group(course):
    current_academic_term = frappe.db.get_single_value("Education Settings","current_academic_term")
    student = frappe.db.get_value("Student", {"user": frappe.session.user}, ['name'])
    if not student: return None
    groups = frappe.db.sql("""
        SELECT grp.name, grp.virtual_room_link FROM `tabStudent Group` as grp
        INNER JOIN `tabStudent Group Student` as grpStd ON grpStd.parent=grp.name
        WHERE grp.academic_term=%(term)s AND grp.course=%(course)s AND grpStd.student=%(student)s AND grpStd.active=1
    """, {"student": student, "course": course.name, "term": current_academic_term}, as_dict=True)
    if len(groups) > 0:
        return groups[0]