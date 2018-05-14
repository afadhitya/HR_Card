{
	'name': 'Employee Card',
	'description': 'Crete Your Own Employee Card',
	'author': 'KELOMPOK B2',
	'depends': ['base', 'mail', 'hr', 'report', 'barcodes'],
	'data': [
		'security/card_security.xml',
		'security/ir.model.access.csv',
		'reports/print_card.xml',
		'reports/report_card_template.xml',
		'reports/print_business_card.xml',
		'reports/report_business_card_template.xml',
		'views/card_menu.xml',
		'views/card_view.xml',
	],
	'application': False,
}
