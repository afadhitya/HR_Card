from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
import logging	

class IdCard(models.Model):
	_name = 'id.card'
	_description = 'Model for Idcard'


	company_name = fields.Char(string='the name of company')
	employee_name = fields.Char(string='your identity')
	'''
	employee_picture = openerp.fields.Binary("Small-sized photo", attachment=True,
    	 			   help="Small-sized photo of the test. It is automatically "\
     	 	    	   "resized as a 64x64px image, with aspect ratio preserved. "\
         	           "Use this field anywhere a small image is required.")
	'''
	employment = fields.Char(string='work')
	origin_department = fields.Char(string='departemen asal')
	gender = fields.Boolean('male/female', default=True)
	date_of_birth = fields.Date('birthday')
	employee_address = fields.Char(string='address the epmloyee')
	employee_email = fields.Char(string='email of employee')
	'''
	employee_contact fields.Char(string='contact the employee')
	Barcode = fields.char(string='---', 'barcode')
	'''