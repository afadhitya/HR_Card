from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BusinessCard(models.Model):
	_name = 'business.card'
	_description = 'Model for Business Card'

	#Employee Information
	company_name = fields.Char(string='Company')
	employee_name = fields.Char(string='Employee')
	job_title = fields.Char(string='Job Title')
	
	#Card Information
	card_Type = fields.selection((('1','Business Card'),('2','Id Card')),string='Card Type')
	card_Id = fields.Integer(string='Card No')
	request_Date= fields.Date(string='Request Date', default=datetime.now())
	reason = fields.Char(string='Reason')
	status	= fields.Char(string='Status')
	active_Periode = fields.Date(string='Active Periode') 
