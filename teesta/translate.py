import frappe

def make_translation_property(args, ignore_validate=False, validate_fields_for_doctype=True):
	"""Create a new **Property Setter** (for overriding DocType and DocField properties)."""
	args = frappe._dict(args)
	tp = frappe.get_doc({
		'doctype': "Translation Property",
		'doctype_or_field': args.doctype_or_field or "DocField",
		'doc_type': args.doctype,
		'field_name': args.fieldname,
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
						"ref_docname": "All",
						"field": field
					}, "name")

	if translations:
		enable_disable_user_translation(doctype=doctype, field=field, is_enabled=1)
		return

	languages = frappe.db.get_values("Language", {"is_active":1}, "language_code")
	languages = [lang[0] for lang in languages]

	sources = options.split("\n")
	for source in sources:
		make_user_translation(doctype=doctype, field=field, source=source, languages=languages)

def make_user_translation(doctype=None, docname="All", field=None, source=None, languages=[]):
	if not all([doctype, field, source]):
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
		lt.target_name = source

	translation.insert(ignore_permissions=True)

def enable_disable_user_translation(doctype=None, docname=None, field=None, lang=None, is_enabled=0):
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
						lt.parent=ut.name %s set is_enabled=%s"""%(build_conditions(), is_enabled)
	frappe.db.sql(update_query, auto_commit=True)