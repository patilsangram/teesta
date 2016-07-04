# -*- coding: utf-8 -*-
# Copyright (c) 2015, Makarand B. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import teesta
from frappe import _
from frappe.utils import cint
from frappe.model.document import Document

doctype_properties = {
	'enable_user_translation': 'Check'
}

docfield_properties = {
	'idx': 'Int',
	'label': 'Data',
	'fieldtype': 'Select',
	'options': 'Text',
	'translate': 'Check'
}

allowed_property = ["enable_user_translation", "translate"]

class CustomizeTranslation(Document):
	def on_update(self):
		frappe.db.sql("delete from tabSingles where doctype='Customize Translation'")
		frappe.db.sql("delete from `tabCustomize Translation Field`")

	def fetch_to_customize(self):
		self.clear_existing_doc()
		if not self.doc_type:
			return

		meta = frappe.get_meta(self.doc_type)

		# translation properties
		translation_enabled = frappe.db.get_value("Translation Property", 
			{ "doc_type":self.doc_type, "property": "enable_user_translation" }, "value") or 0
		self.set("enable_user_translation", translation_enabled)

		for d in meta.get("fields"):
			new_d = {"fieldname": d.fieldname, "name": d.name}
			for property in docfield_properties:
				if property != "translate":
					val = d.get(property)
				else:
					val = frappe.db.get_value("Translation Property", {"doc_type":self.doc_type,
							"property":"translate", "field_name": d.fieldname}, "value") or 0
				new_d[property] = val
			self.append("fields", new_d)

		# NOTE doc is sent to clientside by run_method

	def clear_existing_doc(self):
		doc_type = self.doc_type

		for fieldname in self.meta.get_valid_columns():
			self.set(fieldname, None)

		for df in self.meta.get_table_fields():
			self.set(df.fieldname, [])

		self.doc_type = doc_type
		self.name = "Customize Translation"

	def save_customization(self):
		if not self.doc_type:
			return

		self.set_translation_properties()
		frappe.msgprint(_("{0} updated").format(_(self.doc_type)))
		self.fetch_to_customize()

	def set_translation_properties(self):
		# doctype property setters
		if not self.enable_user_translation:
			self.reset_to_defaults()
			return

		# check if atlease 1 translate is checked
		translation_fields = filter(lambda df: df.translate == 1, self.fields)
		if not translation_fields:
			frappe.throw("Please enable atleast 1 field for translation")

		properties = filter(lambda property: property in allowed_property, doctype_properties.keys())
		for property in properties:
			self.make_property_setter(property=property, value=self.get(property),
				property_type=doctype_properties[property])

		for field in self.fields:
			properties = filter(lambda property: property in allowed_property, docfield_properties.keys())
			for property in properties:
				self.make_property_setter(property=property, value=field.get(property),
					property_type=docfield_properties[property], fieldname=field.fieldname)

	def make_property_setter(self, property, value, property_type, fieldname=None):
		if not self.is_valid_value(value, property_type):
			return

		self.delete_existing_translation_property(property, fieldname)

		# create a new traslation property
		teesta.make_translation_property({
			"doctype": self.doc_type,
			"doctype_or_field": "DocField" if fieldname else "DocType",
			"fieldname": fieldname,
			"property": property,
			"value": value,
			"property_type": property_type
		}, ignore_validate=True)

	def is_valid_value(self, value, property_type):
		flag = False
		if property_type in ["Int", "Check"]:
			flag = True if cint(value) else False
		else:
			flag = True

		return flag

	def delete_existing_translation_property(self, property, fieldname=None):
		# first delete existing property setter
		existing_property_setter = frappe.db.get_value("Translation Property", {"doc_type": self.doc_type,
			"property": property, "field_name['']": fieldname or ''})

		if existing_property_setter:
			frappe.db.sql("delete from `tabTranslation Property` where name=%s", existing_property_setter)

	def reset_to_defaults(self):
		if not self.doc_type:
			return

		frappe.db.sql("""delete from `tabTranslation Property` where doc_type=%s""", self.doc_type)
		self.fetch_to_customize()