// Copyright (c) 2016, New Indictrans Technologies Pvt Ltd. and contributors
// For license information, please see license.txt
frappe.provide("frappe.customize_translation");

frappe.ui.form.on('Customize Translation', {
	onload: function(frm) {
		console.log(frm.doc.doc_type)
		frm.set_query("doc_type", function() {
			return {
				filters: [
					['DocType', 'issingle', '=', 0],
					['DocType', 'custom', '=', 0],
					['DocType', 'name', 'not in', 'DocType, DocField, DocPerm, User, Role, UserRole, \
						 Page, Page Role, Module Def, Print Format, Report, Customize Form, \
						 Customize Form Field', 'Customize Translation', 'Customize Translation Field']
				]
			};
		});

		$(frm.wrapper).on("grid-row-render", function(e, grid_row) {
			if(grid_row.doc && grid_row.doc.fieldtype=="Section Break") {
				$(grid_row.row).css({"font-weight": "bold"});
			}
		});

		$(frm.wrapper).on("grid-make-sortable", function(e, frm) {
			frm.trigger("setup_sortable");
		});
	},

	doc_type: function(frm) {
		if(frm.doc.doc_type) {
			return frm.call({
				method: "fetch_to_customize",
				doc: frm.doc,
				callback: function(r) {
					frm.refresh();
					frm.trigger("setup_sortable");
				}
			});
		}
	},

	setup_sortable: function(frm) {
		frm.doc.fields.forEach(function(f, i) {
			var data_row = frm.page.body.find('[data-fieldname="fields"] [data-idx="'+ f.idx +'"] .data-row');

			if(!f.is_custom_field) {
				data_row.removeClass('sortable-handle');
			} else {
				data_row.addClass("highlight");
			}
		});
	},

	refresh: function(frm) {
		frm.disable_save();
		frm.page.clear_icons();

		if(frm.doc.doc_type) {
			frappe.customize_translation.set_primary_action(frm);

			frm.add_custom_button(__('Refresh Form'), function() {
				frm.script_manager.trigger("doc_type");
			}, "icon-refresh", "btn-default");

			frm.add_custom_button(__('Reset to defaults'), function() {
				frappe.customize_translation.confirm(__('Remove all customizations?'), frm);
			}, "icon-eraser", "btn-default");
		}

		if(frappe.route_options) {
			setTimeout(function() {
				frm.set_value("doc_type", frappe.route_options.doctype);
				frappe.route_options = null;
			}, 1000);
		}

	},
});

frappe.customize_translation.set_primary_action = function(frm) {
	frm.page.set_primary_action(__("Update"), function() {
		if(frm.doc.doc_type) {
			return frm.call({
				doc: frm.doc,
				freeze: true,
				method: "save_customization",
				callback: function(r) {
					if(!r.exc) {
						frm.refresh();
					}
				}
			});
		}
	});
};

frappe.customize_translation.confirm = function(msg, frm) {
	if(!frm.doc.doc_type) return;

	var d = new frappe.ui.Dialog({
		title: 'Reset To Defaults',
		fields: [
			{fieldtype:"HTML", options:__("All customizations will be removed. Please confirm.")},
		],
		primary_action: function() {
			return frm.call({
				doc: frm.doc,
				method: "reset_to_defaults",
				callback: function(r) {
					if(r.exc) {
						msgprint(r.exc);
					} else {
						d.hide();
					}
				}
			});
		}
	});

	frappe.customize_translation.confirm.dialog = d;
	d.show();
}