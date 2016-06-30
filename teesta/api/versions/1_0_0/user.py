import json
import frappe
from teesta.api.request import validate_request
from teesta.api.utils import get_formatted_doc, send_mail
from api_handler.api_handler.exceptions import ValidationError

@frappe.whitelist(allow_guest=True)
def register_user(data):
	# register new user to teesta
	from frappe.utils import random_string
	doc = None
	try:
		response = frappe._dict({})
		args = json.loads(data)
		validate_request("register_user", "1_0_0", args)

		if frappe.db.get_value("User", args.get("email")):
			raise ValidationError("User {0} is already registered".format(args.get("email")))

		doc = frappe.new_doc("User")
		doc.enabled = 0
		doc.no_welcome_mail = True
		doc.new_password = password 		# setting temporary password
		doc.update(args)

		if "flags" in args:
			del args["flags"]

		doc.insert(ignore_permissions=True)

		response.data = get_formatted_doc(doc)
		response.message = "User Created"

		# prepare mail args
		mail_args = frappe._dict({})
		mail_args.user = doc.name
		password = random_string(10)
		mail_args.password = password
		mail_args.link = "#"

		send_mail("verify_email", mail_args, "[Teesta] Verify your account")

		return response

	except Exception, e:
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

@frappe.whitelist(allow_guest=True)
def verify_email(data):
	pass
