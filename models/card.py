from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
from odoo import tools, _
from odoo.modules.module import get_module_resource
import logging

class PrintCard(models.Model):
	_name = 'hr.card'
	_description = 'Model for print card.'

	@api.model
	def _current_department(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.department_id

	@api.model
	def _current_user(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.id

	@api.model
	def _current_job(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.job_id
		

	#Employee Information
	
	employee_ids = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', default=_current_user, readonly=True)
	department_id = fields.Many2one('hr.department', string='Department', default=_current_department, readonly=True)
	job_title = fields.Many2one('hr.job', string='Job Title', default=_current_job, readonly=True)
	
	logo = fields.Binary(string="Company Logo", default=_current_user, readonly=True)


	#Card Information
	card_Type = fields.Selection((
		('business_card', 'Business Card'),
		('id_card','Id Card')
	), string='Card Type', required=True)
	card_Id = fields.Char(string='Card No')
	request_Date= fields.Date(string='Requested Date', default=datetime.now(), readonly=True)
	description = fields.Text('Notes', required=True)
	status = fields.Selection((
		('permanent', 'Permanent'),
		('temporary','Temporary')
	), string='Status')
	active_Periode = fields.Date(string='Expiry Date')

	state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Approval'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('refuse', 'Refused'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

	@api.one
	def do_send_approval(self):
		self.write({'state': 'waiting'})
		return True

	@api.one
	def do_approve(self):
		self.write({'state': 'progress'})
		return True

	@api.one
	def do_refuse(self):
		self.write({'state': 'refuse'})
		return True

	@api.one
	def do_done(self):
		self.write({'state': 'done'})
		return True
