from odoo import models, fields,api


class CiconUserIdentityType(models.Model):
    _name = 'cicon.user.identity.type'
    _description = "CICON User Identity"

    name = fields.Char('Identity Type', required=True)

    _sql_constraints = [('unique_type', 'UNIQUE(name)', 'Identity Type should be Unique!')]


class CiconPasswordCode(models.Model):
    _name = 'cicon.password.code'
    _description = "CICON Password Code"

    name = fields.Char('Password Code', required=True)
    pword = fields.Char('Password ', required=True, groups='cicon_equipment.group_cicon_it_admin')

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'Password Code should be Unique!')]


class CiconUserIdentity(models.Model):
    _name = 'cicon.user.identity'
    _description = "CICON User Identity"

    _inherit = ['mail.thread']

    name = fields.Char('Title', required=True, track_visibility='onchange')
    identity_type_id = fields.Many2one('cicon.user.identity.type', string="Identity Type", required=True, track_visibility='onchange')
    user_name = fields.Char('User Id / Name', track_visibility='onchange')
    pword_type = fields.Selection([('text', 'Text'), ('code', 'Code')], default='text', string="Password Type", track_visibility='onchange')
    pword_text = fields.Char('Password (Text)', track_visibility='onchange', copy=False)
    pass_code_id = fields.Many2one('cicon.password.code', string='Password Code', track_visibility='onchange', copy=False)
    notes = fields.Text('Notes')
    user_id = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user.id, required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id)
    related_equipment_ids = fields.Many2many('maintenance.equipment', 'cicon_equipment_user_identity_rel',
                                         'user_identity_id', 'equipment_id', string='Equipments', readonly=True)
    active = fields.Boolean('Active',default=True, track_visibility='onchange')
    assigned_employee_id = fields.Many2one('hr.employee', 'Employee Assigned')

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'Title should be Unique!')]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = "%s (copy)" % self.name
        return super(CiconUserIdentity, self).copy(default=default)


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    user_identity_ids = fields.Many2many('cicon.user.identity', 'cicon_equipment_user_identity_rel',
                                         'equipment_id', 'user_identity_id', string='User Identities')
