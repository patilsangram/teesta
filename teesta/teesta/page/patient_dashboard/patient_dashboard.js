frappe.pages['patient-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Patient Dashboard',
		single_column: true
	});
	wrapper.patient = new patient(wrapper)
}

patient = Class.extend({
	init: function(wrapper) {
		this.page = wrapper.page
		this.wrapper = $(wrapper).find('.page-content');
		this.set_primary_action();
		this.get_patient_data();
	},

	set_primary_action: function() {
		this.page.set_primary_action(__("Add Patient"), function() {
			doc = frappe.model.get_new_name("Patient Profile")
			frappe.set_route("Form", "Patient Profile", doc);
		});
	},

	get_patient_data: function() {
		console.log(this.page,"t")
		this.page.main.append(frappe.render_template("patient_dashboard"));
	},

})

/*frappe.pages['patient-listing'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Patient Listing',
		single_column: true
	});
	wrapper.patient = new patient(wrapper)
}

patient = Class.extend({
	init: function(wrapper) {
		this.page = wrapper.page
		this.wrapper = $(wrapper).find('.page-content');
		this.set_primary_action();
		this.get_data();
	},

	set_primary_action: function() {
		this.page.set_primary_action(__("Add Patient"), function() {
			doc = frappe.model.get_new_name("Patient")
			frappe.set_route("Form", "Patient", doc);
		});
	},
	
	get_data: function() {
		var me = this;
		frappe.call({
			method: "teesta.teesta.page.patient_listing.custom_methods.get_patient_data",
			callback: function(r) {
				console.log("get_patient_data");
				me.render_template();
			}
		})
	},

	render_template: function() {
		console.log("render_template")
		this.wrapper.append(frappe.render_template("patient_list"));	
	}
});
*/