import frappe
from frappe.utils import get_datetime
from .translate import make_user_translation
from frappe.defaults import get_global_default, set_global_default
from .translate import get_translation_enable_doctypes, get_translation_enable_fields

def make_user_translations():
	""" make user translation for the translation enable doctypes """

	doctypes = get_translation_enable_doctypes()
	if not doctypes:
		return

	for doctype in doctypes:
		fields = get_translation_enable_fields(doctype=doctype, ignore_select=True)
		if not fields:
			continue
		
		key = "__translation::{doctype}".format(doctype=frappe.scrub(doctype))
		max_date = get_global_default(key)

		filters = None
		if max_date:
			filters = { "modified":[">", max_date] }

		dates = []
		fields.append("modified")
		
		docs = frappe.get_all(doctype, filters=filters, fields=fields)
		if not docs:
			continue
		
		for field in fields:
			if field == "modified":
				dates = list(set([get_datetime(doc.get(field)) for doc in docs if doc.get(field, None)]))
			else:
				sources = list(set([doc.get(field) for doc in docs if doc.get(field, None)]))

			for source in sources:
				make_user_translation(doctype=doctype, field=field, source=source)

		max_date = max(dates)
		set_global_default(key, max_date)