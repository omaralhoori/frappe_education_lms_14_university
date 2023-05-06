import hashlib
import frappe
from frappe import _
from frappe.utils.data import cint

def get_enrolled_courses():
    student = frappe.db.get_value("Student", {"user": frappe.session.user}, "name")
    if not student: frappe.throw(_('You are not allowed to view this page!'))
    
    courses = frappe.db.sql("""
        SELECT crs.course_name as title, crs.name as name, crsEnrl.enrollment_status, crs.hero_image as image, crsEnrl.enrollment_date, crsEnrl.program  FROM `tabCourse Enrollment` as crsEnrl
        INNER JOIN `tabCourse` as crs ON crs.name=crsEnrl.course
        WHERE crsEnrl.student=%(student)s AND crsEnrl.enrollment_status IN ('Enrolled', 'Partially Pulled')
    """, {"student": student}, as_dict=True)

    return courses


def get_instructors(course):
    student = frappe.db.get_value("Student", {"user": frappe.session.user}, ["name"])
    academic_year = frappe.db.get_single_value("Education Settings", "current_academic_year")
    academic_term = frappe.db.get_single_value("Education Settings", "current_academic_term")
    instructor_details = frappe.db.sql("""
        SELECT instr.instructor_name as full_name, instr.image as user_image
        FROM `tabStudent Group Instructor` AS grpInstr
        INNER JOIN `tabInstructor` as instr ON instr.name=grpInstr.instructor
        INNER JOIN `tabStudent Group` as stdGrp ON stdGrp.name=grpInstr.parent
        INNER JOIN `tabStudent Group Student` as grpStd ON grpStd.parent=stdGrp.name
        WHERE grpStd.student=%(student)s AND grpStd.active=1 AND stdGrp.course=%(course)s 
            AND stdGrp.academic_year=%(academic_year)s AND stdGrp.academic_term=%(academic_term)s
    """, {"student": student, "course": course, "academic_year": academic_year, "academic_term": academic_term}, as_dict=True)
    return instructor_details


def get_palette(full_name):
	"""
	Returns a color unique to each member for Avatar"""

	palette = [
		["--orange-avatar-bg", "--orange-avatar-color"],
		["--pink-avatar-bg", "--pink-avatar-color"],
		["--blue-avatar-bg", "--blue-avatar-color"],
		["--green-avatar-bg", "--green-avatar-color"],
		["--dark-green-avatar-bg", "--dark-green-avatar-color"],
		["--red-avatar-bg", "--red-avatar-color"],
		["--yellow-avatar-bg", "--yellow-avatar-color"],
		["--purple-avatar-bg", "--purple-avatar-color"],
		["--gray-avatar-bg", "--gray-avatar-color0"],
	]

	encoded_name = str(full_name).encode("utf-8")
	hash_name = hashlib.md5(encoded_name).hexdigest()
	idx = cint((int(hash_name[4:6], 16) + 1) / 5.33)
	return palette[idx % 8]


def redirect_to_courses_list():
	frappe.local.flags.redirect_location = "/courses"
	raise frappe.Redirect
