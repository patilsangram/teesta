import frappe

def get_formatted_doc(doc, fields=[], version="1_0_0"):
	""" get doc as per schema """
	if not fields: fields = get_allowed_fields(doc.doctype, version)
	_doc = doc.as_dict()

	if not fields:
		return _doc
	else:
		[_doc.pop(field) for field in _doc.keys() if field not in fields]
		return _doc