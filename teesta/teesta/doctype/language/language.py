# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans Technologies Pvt Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Language(Document):
	"""Language Master, enable or disable language"""

	def validate(self):
		""" disable/enable all the translation if Is Activated = 0 or 1 """

		query = """ update `tabLanguage Translation` set is_enabled={is_active} where
					language='{language}'""".format(
						is_active=self.is_active,
						language=self.language_code
					)

		frappe.db.sql(query, auto_commit=True)