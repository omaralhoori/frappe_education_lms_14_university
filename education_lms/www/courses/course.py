
import frappe
from education_lms.education_lms.utils import redirect_to_courses_list

def get_context(context):
    context.no_cache = 1
    print("sssssssssssssssssssss")
    try:
        course_name = frappe.form_dict["course"]
        print(course_name)
    except KeyError:
        redirect_to_courses_list()