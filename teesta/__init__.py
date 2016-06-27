# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import json
import frappe
import api_handler
from frappe.utils import cstr, cint
from api_handler.response import report_error

__version__ = '0.0.1'

@frappe.whitelist(allow_guest=True)
def login(data):
	user_data = json.loads(data)
	try: 
		if user_data.get("usr") and user_data.get("pwd"):
			frappe.clear_cache(user = user_data["usr"])
			frappe.local.login_manager.authenticate(user_data["usr"],user_data["pwd"])
			frappe.local.login_manager.post_login()
			frappe.response["sid"] = frappe.session.sid
			frappe.response["message"] = "Logged In"
		else:
			raise api_handler.InvalidDataError("Invalid Input")
	except frappe.AuthenticationError,e:
		http_status_code = getattr(e, "http_status_code", 500)
		frappe.response["code"] = http_status_code
	finally:
		ts = int(time.time())
		frappe.response["timestamp"] = ts