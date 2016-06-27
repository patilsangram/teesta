import json
import frappe
from teesta.api.schema import get_allowed_fields
from api_handler.api_handler.exceptions import InvalidDataError

@frappe.whitelist()
def handle(resource, data=None, version="1_0_0", req_method="GET",
			filters=None, limit_start=None, limit_page_length=20):
	def get():
		""" get doc and return """
		doc = frappe.get_doc(doctype, docname)

		if not doc.has_permission("read"):
			raise frappe.PermissionError

		doc = doc.as_dict()
		[doc.pop(field) for field in doc.keys() if field not in fields]
		result.append(doc)
		response.message = "Resource Fetched"

	def save():
		""" insert or update doc """
		# Todo check permissions
		raise NotImplementedException
		doc = None

		if not data:
			raise InvalidDataError

		args = json.loads(data)
		if "ignore_permissions" in args: args.pop("ignore_permissions")
		if "flags" in args: del args["flags"]

		if not doctype:
			raise InvalidDataError("Invalid URL")

		if not docname and req_method == "POST":
			args.update({ "doctype": doctype })
			doc = frappe.get_doc(args).insert().as_dict()
		elif req_method == "PUT":
			doc = frappe.get_doc(doctype, docname)
			doc.update(args)
			doc = doc.save().as_dict()

		frappe.db.commit()

		[doc.pop(field) for field in doc.keys() if field not in fields]

		result.append(doc)
		response.message = "Resource Saved"

	def delete():
		""" delete the doc """
		raise NotImplementedException
		if not doc.has_permission("delete"):
			raise frappe.PermissionError

		frappe.delete_doc(doctype, name)
		frappe.db.commit()
		response.message = "Resource Delete"

	result = []
	response = frappe._dict({})
	methods = {
		"GET": get,
		"POST": save,
		"PUT": save,
		"DELETE": delete
	}

	try:
		if not isinstance(resource, dict): resource = json.loads(resource)
		if not resource:
			raise Exception("Doctype, Docname is missing")

		doctype = resource.get("doctype", None)
		docname = resource.get("docname", None)
		fields = get_allowed_fields(doctype, version)

		if all([doctype, docname]):
			methods[req_method]()
		elif all([doctype, req_method == "GET"]):
			# TODO check permissions
			result = frappe.get_list(
						doctype, filters=filters, fields=fields,
						limit_start=limit_start, limit_page_length=limit_page_length
					)
		else:
			raise frappe.DoesNotExistError

		if req_method in ["GET", "POST", "PUT"]: response.data = result
		return response
	except Exception, e:
		import traceback
		print traceback.print_exc()
		raise e