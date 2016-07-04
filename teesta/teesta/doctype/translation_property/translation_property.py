# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans Technologies Pvt Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TranslationProperty(Document):
	def autoname(self):
		self.name = self.doc_type + "-" \
			+ (self.field_name and (self.field_name + "-")  or "") \
			+ self.property
