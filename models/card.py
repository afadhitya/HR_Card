from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
from odoo import tools, _
from odoo.modules.module import get_module_resource
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

	@api.model
	def _default_image(self):
		image_path = get_module_resource('hr','static/src/img','default_image.png')
		return tools.image_resize_image_big(open(image_path,'rb').read().encode('base64')) 

	#Employee Information
	company_id = fields.Many2one('res.company', 'Company', default=_current_user,readonly=True)
	employee_ids = fields.Many2one('res.users', string='Employee', track_visibility='onchange', default=_current_user,readonly=True)
	department_id = fields.Many2one('hr.department', string='Department', default=_current_department, readonly=True)
	job_title = fields.Many2one('hr.job', string='Job Title', default=_current_job, readonly=True)
	address_home_id = fields.Many2one('res.partner', string='Home Address')

	image = fields.Binary(string="Photo", default=_default_image, attachment=True, help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
	image_medium = fields.Binary("Medium-sized photo", attachment=True,
        help="Medium-sized photo of the employee. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
	#Card Informationr
	card_Type = fields.Selection((('business_card','Business Card'),('id_card','Id Card')),string='Card Type', required=True)
	card_Id = fields.Integer(string='Card No')
	request_Date= fields.Date(string='Request Date', default=datetime.now(), readonly=True)
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






    	
    

