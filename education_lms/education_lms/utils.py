import hashlib
from education_lms.education_lms.md import markdown_to_html
import frappe
from frappe import _
from frappe.utils.data import cint
import re
from urllib.parse import urlparse
from urllib.parse import parse_qs


RE_SLUG_NOTALLOWED = re.compile("[^a-z0-9]+")


def slugify(title, used_slugs=None):
	"""Converts title to a slug.

	If a list of used slugs is specified, it will make sure the generated slug
	is not one of them.

	    >>> slugify("Hello World!")
	    'hello-world'
	    >>> slugify("Hello World!", ['hello-world'])
	    'hello-world-2'
	    >>> slugify("Hello World!", ['hello-world', 'hello-world-2'])
	    'hello-world-3'
	"""
	if not used_slugs:
		used_slugs = []

	slug = RE_SLUG_NOTALLOWED.sub("-", title.lower()).strip("-")
	used_slugs = set(used_slugs)

	if slug not in used_slugs:
		return slug

	count = 2
	while True:
		new_slug = f"{slug}-{count}"
		if new_slug not in used_slugs:
			return new_slug
		count = count + 1


def get_enrolled_courses():
    student = frappe.db.get_value("Student", {"user": frappe.session.user}, "name")
    if not student: frappe.throw(_('You are not allowed to view this page!'))
    
    courses = frappe.db.sql("""
        SELECT crs.course_name as title, crs.name as name, crsEnrl.enrollment_status, crs.hero_image as image, crsEnrl.enrollment_date, crsEnrl.program, crsEnrl.progress  FROM `tabCourse Enrollment` as crsEnrl
        INNER JOIN `tabCourse` as crs ON crs.name=crsEnrl.course
        WHERE crsEnrl.student=%(student)s AND crsEnrl.enrollment_status IN ('Enrolled', 'Partially Pulled')
    """, {"student": student}, as_dict=True)

    return courses

def get_live_courses(enrolled_courses):
	enrolled_courses = [f'"{course.name}"' for course in enrolled_courses]
	where_stmt = ""
	if len(enrolled_courses) > 0:
		where_stmt = "WHERE name not in ({enrolled_courses})".format(enrolled_courses=",".join(enrolled_courses))
	courses = frappe.db.sql("""
		select crs.course_name as title, crs.name as name, crs.hero_image as image
		FROM `tabCourse` as crs
		{where_stmt}
	""".format(where_stmt=where_stmt), as_dict=True)
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


def redirect_to_courses_list(redirect_to='/courses'):
	frappe.local.flags.redirect_location = redirect_to
	raise frappe.Redirect


def get_course_progress(course_name, user):
	student = frappe.db.get_value("Student", {"user": user}, ["name"])
	if not student: return frappe._dict({"course_enabled": False})
	progress = frappe.db.get_value("Course Enrollment", {"course": course_name, "enrollment_status": ["IN", "Enrolled,Partially Pulled"]}, [
			"current_lesson_type", "current_lesson", "progress"
	], as_dict=True)
	if progress: return frappe._dict({"course_enabled": True, "progress": progress})
	return frappe._dict({"course_enabled": False})


def get_lessons(course, topic=None):
	"""If chapter is passed, returns lessons of only that chapter.
	Else returns lessons of all chapters of the course"""
	lessons = []
	
	if topic:
		return get_lesson_details(topic)
	topics = get_topics(course)
	for topic in topics:
		lesson = get_lesson_details(topic, topic.idx)
		lessons += lesson
	return lessons




def get_lesson_details(topic, parent_idx=1):
	lessons = []
	lesson_list = frappe.get_all(
		"Topic Content", {"parent": topic.name}, ["content_type","content", "idx"], order_by="idx"
	)

	for row in lesson_list:
		lesson_details = frappe.db.get_value(
			row.content_type,
			row.content,
			get_lesson_fields(row.content_type),
			as_dict=True,
		)
		# lesson_details.number = flt(f"{chapter.idx}.{row.idx}")
		lesson_details.icon = get_lesson_icon(row.content_type)
		lesson_details.content_type = row.content_type
		lesson_details.content = row.content
		lesson_details.idx = f"{parent_idx}.{row.idx}"
		# macros = find_macros(lesson_details.body)

		# for macro in macros:
		# 	if macro[0] == "YouTubeVideo":
		# 		lesson_details.icon = "icon-video"
		# 	elif macro[0] == "Quiz":
		# 		lesson_details.icon = "icon-quiz"
		lessons.append(lesson_details)
	return lessons

def get_lesson_fields(lesson_type):
	if lesson_type == 'Article':
		return [
				"name",
				"title",
				"content as body"
			]
	elif lesson_type == 'Video':
		return [
			"name",
			"title",
			"url",
			"provider",
			"description"
		]
	else:
		return [
			"name"
		]
def get_lesson_icon(lesson_type):
	if lesson_type == 'Video':
		return 'icon-image'
	else: return 'icon-list'
def show_start_learing_cta(course, membership):
	show_button = True

	return show_button


def get_topics(course):
	topics = frappe.db.sql("""
		SELECT tpc.name, tpc.topic_name, tpc.description, crsTpc.idx FROM `tabCourse Topic` as crsTpc
		INNER JOIN `tabTopic` as tpc ON crsTpc.topic=tpc.name
		WHERE crsTpc.parent=%(course)s
	""", {"course": course}, as_dict=True)
	return topics

def get_progress(course, lesson_type, lesson):
	student = frappe.db.get_value("Student", {"user": frappe.session.user}, "name")
	if not student: return
	course_enrollment = frappe.db.get_value("Course Enrollment", {"student": student, "course": course, "enrollment_status": ["in", ["Enrolled", "Partially Pulled"]]})
	if not course_enrollment:
		frappe.msgprint(_("You are not enrolled in this course"))
		return 'Not Completed'
	if frappe.db.exists("Course Activity", {"enrollment": course_enrollment, "content_type": lesson_type, "content": lesson}):
		return 'Complete'
	else:
		return 'Not Completed'
def get_slugified_chapter_title(chapter):
	s = slugify(chapter)
	return s

def get_lesson_url(course,  lesson_type, lesson):
	return f"/lessons?course={course}&lesson-type={lesson_type}&lesson={lesson}"




def render_html(lesson):
	body = lesson.body or ""
	youtube = None
	if lesson.content_type == 'Video':	
		youtube = lesson.url
		body = lesson.description
	quiz_id = lesson.quiz_id
	

	if youtube and "/" in youtube:
		parsed_url = urlparse(youtube)
		if len(parse_qs(parsed_url.query)['v']) > 0:
			youtube = parse_qs(parsed_url.query)['v'][0]


	quiz_id = "{{ Quiz('" + quiz_id + "') }}" if quiz_id else ""
	youtube = "{{ YouTubeVideo('" + youtube + "') }}" if youtube else ""
	text = youtube + body + quiz_id

	if lesson.question:
		assignment = "{{ Assignment('" + lesson.question + "-" + lesson.file_type + "') }}"
		text = text + assignment

	return markdown_to_html(text)