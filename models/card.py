from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
from odoo import tools, _
from odoo.modules.module import get_module_resource
import logging

class PrintCard(models.Model):
	_name = 'print.card'
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
		

	@api.model
	def _current_image(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.image

	@api.model
	def _current_birthday(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.birthday

	@api.model
	def _current_email(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.work_email

	@api.model
	def _current_phone(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.work_phone

	@api.model
	def _current_mobile(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.mobile_phone

	@api.model
	def _current_gender(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.gender

	@api.model
	def _current_home(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))
		return employee.address_home_id

	#Employee Information
	company_id = fields.Many2one('res.company', 'Company', default=_current_user, readonly=True)
	employee_ids = fields.Many2one('res.users', string='Employee', track_visibility='onchange', default=_current_user, readonly=True)
	department_id = fields.Many2one('hr.department', string='Department', default=_current_department, readonly=True)
	job_title = fields.Many2one('hr.job', string='Job Title', default=_current_job, readonly=True)
	address_home_id = fields.Many2one('res.partner', string='Home Address', default=_current_home, readonly=True)
	birthday = fields.Date('Date of Birth', default=_current_birthday, readonly=True)
	work_email = fields.Char('Work Email', default=_current_email, readonly=True)
	work_phone = fields.Char('Work Phone', default=_current_phone, readonly=True)
	mobile_phone = fields.Char('Work Mobile', default=_current_mobile, readonly=True)
	gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default=_current_gender, readonly=True)
	image = fields.Binary(string="Photo", default=_current_image, attachment=True, readonly=True,
		help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
	image_medium = fields.Binary("Medium-sized photo", attachment=True,
        help="Medium-sized photo of the employee. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")

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
	active_Periode = fields.Date(string='Active Periode')

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
