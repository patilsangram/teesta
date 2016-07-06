import frappe

def make_translation_property(args, ignore_validate=False, validate_fields_for_doctype=True):
	"""Create a new **Property Setter** (for overriding DocType and DocField properties)."""
	args = frappe._dict(args)
	tp = frappe.get_doc({
		'doctype': "Translation Property",
		'doctype_or_field': args.doctype_or_field or "DocField",
		'doc_type': args.doctype,
		'field_name': args.fieldname,
		'field_type': args.fieldtype,
		'property': args.property,
		'value': args.value,
		'property_type': args.property_type or "Data",
		'__islocal': 1
	})
	tp.flags.ignore_validate = ignore_validate
	tp.insert()

def make_user_translation_for_select_field(doctype, field, options):
	if not options:
		return

	# check if user translation is already created
	translations = frappe.db.get_values("User Translation", {
						"ref_doctype":doctype,
						"field": field
					}, "name")

	if translations:
		enable_disable_user_translation(doctype=doctype, field=field, value=1)
		return

	languages = frappe.db.get_values("Language", {"is_active":1}, "language_code")
	languages = [lang[0] for lang in languages]

	sources = [opt for opt in options.split("\n") if opt]
	for source in sources:
		make_user_translation(doctype=doctype, field=field, source=source, languages=languages)

def make_user_translation(doctype=None, docname="All", field=None, source=None, languages=[]):
	if not all([doctype, field, source]):
		return

	# check if translation doc is already created for source
	name = frappe.db.get_value("User Translation", {
				"ref_docname": docname,
				"ref_doctype": doctype,
				"field": field
			})
	if all([docname, docname != "All", name]):
		frappe.get_doc({
			"doctype": "User Translation",
			"docname": name,
			"is_updated": "1"
		}).save(ignore_permissions=True)
		enable_disable_user_translation(doctype=doctype, docname=docname, field=field, update_enabled=False)
		return

	translation = frappe.new_doc("User Translation")
	translation.field = field
	translation.ref_docname = docname
	translation.ref_doctype = doctype
	translation.source_name = source

	translation.set("translations", [])

	for language in languages:
		# create child table entry
		lt = translation.append("translations", {})
		lt.is_enabled = 1
		lt.language = language
		lt.target_name = ''

	translation.insert(ignore_permissions=True)

def enable_disable_user_translation(doctype=None, docname=None, field=None, lang=None, update_enabled=True, value=0):
	def is_multiple(items):
		op = "="
		val = "'%s'"%(items)
		if isinstance(items, list):
			op = " in "
			val = "(%s)"%(",".join(["'%s'"%(item) for item in items]))

		return {
			"op": op,
			"val": val
		}

	def build_conditions():
		condition = ""
		if doctype:
			condition += " and ut.ref_doctype{op}{val}".format(**is_multiple(doctype))
		if docname:
			condition += " and ut.ref_docname{op}{val}".format(**is_multiple(docname))
		if field:
			condition += " and ut.field{op}{val}".format(**is_multiple(field))
		if lang:
			condition += " and lt.language{op}{val}".format(**is_multiple(lang))
		return condition

	if not any([doctype, docname, field, lang]):
		frappe.throw("Can't disable translation, Invalid Input !!")

	if not lang:
		languages = frappe.db.get_values("Language", {"is_active":1}, "language_code")
		lang = [language[0] for language in languages]

	update_query = """update `tabLanguage Translation` lt inner join `tabUser Translation` ut on
						lt.parent=ut.name %s set %s=%s"""%(
							build_conditions(),
							"is_enabled" if update_enabled else "is_varified",
							value
						)
	frappe.db.sql(update_query, auto_commit=True)

def get_translation_enable_doctypes():
	""" get all the translation enabled DocType """
	filters = {
		"doctype_or_field": "DocType",
		"property": "enable_user_translation",
		"value": "1"
	}
	doc_types = frappe.db.get_values("Translation Property", filters, "doc_type")
	doc_types = [doctype[0] for doctype in doc_types]
	return doc_types or []

def get_translation_enable_fields(doctype=None, ignore_select=False):
	""" get all translation enabled DocFields """
	doctypes = get_translation_enable_doctypes() if not doctype else [doctype]

	filters = {
		"doctype_or_field": "DocField",
		"property": "translate",
		"doc_type": ["in", doctypes],
		"value": "1",
	}

	if ignore_select:
		filters.update({ "field_type": ["!=", "Select"] })

	fields = frappe.db.get_values("Translation Property", filters, "field_name")
	fields = [field[0] for field in fields]

	return fields or []