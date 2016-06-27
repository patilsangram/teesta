import json
import frappe

to_string_type = ["Long Text", "Password", "Read Only", "Data", "Select", "Small Text", "Text", "Link"]
to_date_type = ["Date", "Datetime"]
to_float_type = ["Currency", "Percent"]
to_int_type = ["Check", "Int"]

# def update_doctype_schema(doc, method):
# 	schema = {}
# 	not_allowed_type = [
# 		"Attach", "Attach Image", "Code","Button", "Column Break", "Dynamic Link",
# 		"Fold", "Heading", "HTML", "Image", "Section Break", "Table", "Text Editor"
# 	]

# 	if doc.module == "bewo":
# 		schema = {field.fieldname: { "reqd": field.reqd, "fieldtype": get_type(field.fieldtype) } for field in doc.fields if field.fieldtype not in not_allowed_type}
# 		app_name = frappe.db.get_value("Module Def", doc.module, "app_name")
# 		path =  frappe.get_app_path(app_name, "api", "schema", "{}.json".format(frappe.scrub(doc.name)))
		
# 		with open(path,"w") as f:
# 			f.write(json.dumps(schema, sort_keys=True, indent=2))

def get_type(_type):
	if _type in to_string_type:
		return "basestring"
	elif _type in to_float_type:
		return "float"
	elif _type in to_int_type:
		return "int"
	elif _type in to_date_type:
		return "date"

def get_schema(resource, version, is_method=False):
	""" get request schema as dict from .json file """
	schema = {}
	resource = resource.lower()
	fname = "{}.json".format(frappe.scrub(resource))

	_dir = "method" if is_method else "resource"

	file_path = frappe.get_app_path("teesta", "api", "versions", version, "schema", _dir, fname)
	with open(file_path, "r") as f:
		schema = json.loads(f.read())

	return schema

def get_allowed_fields(resource, version="1_0_0", is_method=False):
	""" get list of allowed fields """

	schema = get_schema(resource, version, is_method=is_method)
	if not schema:
		raise Exception("Schema not found")

	return schema.get("request_header").keys()