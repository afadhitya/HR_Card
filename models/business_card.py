from odoo import api, fields, models
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError
import logging

class BusinessCard(models.Model):
	_name = 'business.card'
	_description = 'Model for Business Card'

	@api.model
	def _current_department(self):

		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]

		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.department_id

	company_id = fields.Many2one('res.company', 'Company')
	employee_ids = fields.Many2one('res.users', string='Employee', track_visibility='onchange', default=lambda self: self.env.user,readonly=True)
	logo 	= fields.Binary("Small-sized photo", attachment=True,
              help="Small-sized photo of the employee. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
	address = fields.Char(string='to know your life')
	contact = fields.Char(string='contact owner')
	email	= fields.Char(string='to contact in email')
