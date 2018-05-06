from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BusinessCard(models.Model):
	_name = 'print.card'
	_description = 'Model for print'

	company_name = fields.Char(string='the name of company your work')
	employee_name = fields.Char(help="what needs to be done?")
	logo 	= fields.Binary("Small-sized photo", attachment=True,
              help="Small-sized photo of the employee. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
	address = fields.Char(string='to know your life')
	contact = fields.Char(string='contact owner')
	email	= fields.Char(string='to contact in email')
