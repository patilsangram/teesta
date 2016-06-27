import json
import frappe
from teesta.api.request import validate_request
from teesta.api.utils import get_formatted_doc

@frappe.whitelist(allow_guest=True)
def register_user(data):
	# register new user to teesta
	try:
		args = json.loads(data)
		validate_request("register_user", "1_0_0", args)
		doc = frappe.new_doc("User")
		doc.update(args)

		# if "flags" in args:
		# 	del args["flags"]

		doc.save()
		return get_formatted_doc(doc)

	except Exception, e:
		import traceback
		print e
		print traceback.print_exc()
		raise e

@frappe.whitelist(allow_guest=True)
def forgot_password(data):
	# send verification mail to user and reset password
	try:
		args = json.loads(data)
		validate_request("forgot_password", "1_0_0", args)
	except Exception, e:
		raise e

@frappe.whitelist()
def update_password(data):
	# update user's password through api call
	try:
		args = json.loads(data)
		validate_request("update_password", "1_0_0", args)
	except Exception, e:
		raise e
