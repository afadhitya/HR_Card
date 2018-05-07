from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
import logging

class BusinessCard(models.Model):
	_name = 'print.card'
	_description = 'Model for print'

	@api.model
	def _current_department(self):

		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]

		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.department_id

	#Employee Information
	company_id = fields.Many2one('res.company', 'Company')
	employee_ids = fields.Many2one('res.users', string='Employee', track_visibility='onchange', default=lambda self: self.env.user,readonly=True)
	department_id = fields.Many2one('hr.department', string='Department', default=_current_department, readonly=True)
	job_title = fields.Char(string='Job Title')
	
	#Card Information
	card_Type = fields.Selection((('business_card','Business Card'),('id_card','Id Card')),string='Card Type')
	card_Id = fields.Integer(string='Card No')
	request_Date= fields.Date(string='Request Date', default=datetime.now())
	description = fields.Text('Notes',required=True)
	status	= fields.Selection((('permanent','Permanent'),('temporary','Temporary')),string='Status')
	active_Periode = fields.Date(string='Active Periode')

	state = fields.Selection([
        ('new', 'New'),
        ('waiting', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
        ('reject', 'Reject'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='new')

