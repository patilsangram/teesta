# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "teesta"
app_title = "Teesta"
app_publisher = "New Indictrans Technologies Pvt Ltd."
app_description = "Teesta"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "makarand.b@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/teesta/css/teesta.css"
# app_include_js = "/assets/teesta/js/teesta.js"

# include js, css files in header of web template
# web_include_css = "/assets/teesta/css/teesta.css"
# web_include_js = "/assets/teesta/js/teesta.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "teesta.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "teesta.install.before_install"
# after_install = "teesta.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "teesta.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"teesta.tasks.all"
# 	],
# 	"daily": [
# 		"teesta.tasks.daily"
# 	],
# 	"hourly": [
# 		"teesta.tasks.hourly"
# 	],
# 	"weekly": [
# 		"teesta.tasks.weekly"
# 	]
# 	"monthly": [
# 		"teesta.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "teesta.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "teesta.event.get_events"
# }

