from . import __version__ as app_version
from frappe import _
app_name = "education_lms"
app_title = "Education Lms"
app_publisher = "Omar"
app_description = "Learning management system for erpnext education"
app_email = "lms@mail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/education_lms/css/education_lms.css"
# app_include_js = "/assets/education_lms/js/education_lms.js"

# include js, css files in header of web template
# web_include_css = "/assets/education_lms/css/education_lms.css"
# web_include_js = "/assets/education_lms/js/education_lms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "education_lms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js, css files in header of web template
web_include_css = "lms.bundle.css"
# web_include_css = "/assets/lms/css/lms.css"
web_include_js = ["website.bundle.js"]

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
    "education_lms.education_lms.utils.get_instructors",
    "education_lms.education_lms.utils.get_palette",
    "education_lms.education_lms.utils.get_lessons",
    "education_lms.education_lms.utils.show_start_learing_cta",
    "education_lms.education_lms.utils.get_slugified_chapter_title",
    "education_lms.education_lms.utils.get_topics",
    "education_lms.education_lms.utils.get_progress",
    "education_lms.education_lms.utils.render_html",
    "education_lms.education_lms.utils.get_lesson_url",
	],
	#"filters": "education_lms.utils.jinja_filters"
}


## Markdown Macros for Lessons
education_lms_markdown_macro_renderers = {
	"Exercise": "education_lms.plugins.exercise_renderer",
	"Quiz": "education_lms.plugins.quiz_renderer",
	"YouTubeVideo": "education_lms.plugins.youtube_video_renderer",
	"Video": "education_lms.plugins.video_renderer",
	"Assignment": "education_lms.plugins.assignment_renderer",
}


# Installation
# ------------

# before_install = "education_lms.install.before_install"
# after_install = "education_lms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "education_lms.uninstall.before_uninstall"
# after_uninstall = "education_lms.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "education_lms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }


standard_portal_menu_items = [
	{
		"title": _("Enrolled Courses"),
		"route": "/courses",
		"role": "Student",
	},
]



# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"education_lms.tasks.all"
#	],
#	"daily": [
#		"education_lms.tasks.daily"
#	],
#	"hourly": [
#		"education_lms.tasks.hourly"
#	],
#	"weekly": [
#		"education_lms.tasks.weekly"
#	],
#	"monthly": [
#		"education_lms.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "education_lms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "education_lms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "education_lms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


update_website_context = [
	"education_lms.widgets.update_website_context",
]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"education_lms.auth.validate"
# ]
