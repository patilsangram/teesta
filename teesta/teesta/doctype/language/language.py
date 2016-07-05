# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans Technologies Pvt Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from teesta.translate import enable_disable_user_translation

class Language(Document):
	"""Language Master, enable or disable language"""

	def validate(self):
		""" disable/enable all the translation if Is Activated = 0 or 1 """

		query = """ update `tabLanguage Translation` set is_enabled={is_active} where
					language='{language}'""".format(
						is_active=self.is_active,
						language=self.language_code
					)
		if not self.is_active:
			enable_disable_user_translation(lang=self.language_code, is_enabled=self.is_active)
		else:
			# get all the translation enabled DocType
			filters = {
				"doctype_or_field": "DocType",
				"property": "enable_user_translation",
				"value": "1"
			}
			doc_types = frappe.db.get_values("Translation Property", filters, "doc_type")
			doc_types = [doctype[0] for doctype in doc_types]

			if not doc_types:
				enable_disable_user_translation(lang=self.language_code)
				return

			filters = {
				"doctype_or_field": "DocField",
				"property": "translate",
				"doc_type": ["in", doc_types],
				"value": "1",
			}
			fields = frappe.db.get_values("Translation Property", filters, "field_name")
			fields = [field[0] for field in fields]
			
			enable_disable_user_translation(doctype=doc_types, field=fields, lang=self.language_code,
				is_enabled=self.is_active)