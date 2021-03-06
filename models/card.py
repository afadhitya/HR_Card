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
	_inherit = ['mail.thread']

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
	def _current_id(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))

		idcard = str(employee.id)
		dept = str(employee.department_id.id)
		tanggal = datetime.now().strftime("%d%m%y")

		if len(idcard) == 1 :
			idcard ='00'+idcard
		elif len(idcard) == 2:
			idcard ='0'+idcard

		if len(dept) == 1:
			dept = '0'+ dept

		idcard = idcard + dept + tanggal
		return idcard

	@api.model
	def _current_id_access_employee(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))

		idcard = str(employee.id)
		dept = str(employee.department_id.id)
		tanggal = datetime.now().strftime("%d%m%y")

		if len(idcard) == 1 :
			idcard ='00'+idcard
		elif len(idcard) == 2:
			idcard ='0'+idcard

		if len(dept) == 1:
			dept = '0'+ dept

		code = '00'

		idcard = idcard + code + tanggal

		# dict(self.field['using_For']._description_selection(self.evn)).get(self.using_For)
		# self._fields['using_For'].get_values(self.env)
		# dict(self._fields['using_For'].selection).get(self.using_For)


		return idcard

	@api.model
	def _current_id_access_guest(self):
		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]
		_logger = logging.getLogger(__name__)
		_logger.debug('RESOURCE ID: ' + str(employee.name_related))

		idcard = str(employee.id)
		dept = str(employee.department_id.id)
		tanggal = datetime.now().strftime("%d%m%y")

		if len(idcard) == 1 :
			idcard ='00'+idcard
		elif len(idcard) == 2:
			idcard ='0'+idcard

		if len(dept) == 1:
			dept = '0'+ dept

		code = '01'

		idcard = idcard + code + tanggal

		# dict(self.field['using_For']._description_selection(self.evn)).get(self.using_For)
		# self._fields['using_For'].get_values(self.env)
		# dict(self._fields['using_For'].selection).get(self.using_For)


		return idcard


	#Employee Information

	employee_ids = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', default=_current_user)
	department_id = fields.Many2one('hr.department', string='Department', default=_current_department, readonly=True)
	job_title = fields.Many2one('hr.job', string='Job Title', default=_current_job)\

	logo = fields.Binary(string="Company Logo", default=_current_user, readonly=True)


	#Card Information
	card_Type = fields.Selection((
		('business_card', 'Business Card'),
		('id_card','Id Card'),
		('access_card','Access Card')
	), string='Card Type', required=True)
	using_For = fields.Selection((
		('employee', 'Employee'),
		('guest', 'Guest')
	), string='Using For')
	card_Id = fields.Char(string='Card No', default=_current_id, readonly=True)
	card_IdEmployee = fields.Char(string='Card No Employee', default=_current_id_access_employee, readonly=True)
	card_IdGuest = fields.Char(string='Card No Guest', default=_current_id_access_guest, readonly=True)
	request_Date= fields.Date(string='Requested Date', default=datetime.now(), readonly=True)
	description = fields.Text('Notes', required=True)
	status = fields.Selection((
		('permanent', 'Permanent'),
		('temporary','Temporary')
	), string='Status')
	active_Periode = fields.Date(string='Expire Date')

	state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Approval'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('refuse', 'Refused'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

	@api.one
	def do_send_approval(self):
		if self.env['hr.card'].search([('create_uid','=', self.env.uid)]):
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

	@api.multi
	def action_approval_send(self):
		''' Pop Up Compose Email '''
		self.ensure_one()
		ir_model_data = self.env['ir.model.data']
		try:
			template_id = ir_model_data.get_object_reference('HR_Card','email_template_edi_card')[1]
			#template_id = self.env.ref('model.email_template_edi_card')
			#template_id.send_mail(self.ids[0], force_send=True)
		except ValueError:
			template_id = False

		try:
			compose_form_id = ir_model_data.get_object_reference('mail','email_compose_message_wizard_form')[1]
		except ValueError:
			compose_form_id = False

		ctx = dict()
		ctx.update({
			'default_model':'hr.card',
			'default_res_id': self.ids[0],
			'default_use_template': bool(template_id),
			'default_template_id': template_id,
			'default_composition_mode': 'comment',
			'mark_so_as_sent': True,

			})
		self.write({'state': 'waiting'})
		return{
			'type':'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views':[(compose_form_id,'form')],
			'view_id': compose_form_id,
			'target':'new',
			'context': ctx,
		}
