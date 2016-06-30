import frappe
from schema import get_allowed_fields

def get_formatted_doc(doc, fields=[], version="1_0_0"):
	""" get doc as per schema """
	if not fields: fields = get_allowed_fields(doc.doctype, version)
	_doc = doc.as_dict()

	if not fields:
		return _doc
	else:
		[_doc.pop(field) for field in _doc.keys() if field not in fields]
		return _doc

def send_mail(action, args, subject):
	""" send mail """
	from frappe.utils.user import get_user_fullname

	sender = None
	template = "templates/email/verify_email.html"

	try:
		args.update({
			"fullname": get_user_fullname(args.get("user")) or "Guest"
		})

		frappe.sendmail(recipients=args.get("email"), sender=sender, subject=subject,
			message=frappe.get_template(template).render(args))

		return True
	except Exception, e:
		# raise Exception("Error while sending mail")
		return False