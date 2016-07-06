# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans Technologies Pvt Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from teesta.translate import enable_disable_user_translation
from teesta.translate import get_translation_enable_doctypes, get_translation_enable_fields

class Language(Document):
	"""Language Master, enable or disable language"""

	def validate(self):
		""" disable/enable all the translation if Is Activated = 0 or 1 """
		if not self.is_active:
			enable_disable_user_translation(lang=self.language_code, value=self.is_active)
		else:
			# get all the translation enabled DocType
			doc_types = get_translation_enable_doctypes()
			if not doc_types:
				enable_disable_user_translation(lang=self.language_code)
				return

			fields = get_translation_enable_fields()
			enable_disable_user_translation(doctype=doc_types, field=fields, lang=self.language_code,
				value=self.is_active)