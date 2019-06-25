from odoo import models, fields, api


class EquipmentCategoryProperty(models.Model):
    _name = 'equipment.category.property'
    _description = "Equipment Category Property"

    name = fields.Char('Property Name', required=True)

    _sql_constraints = [('uniq_name', 'UNIQUE(name)', "Property Name Should be Unique")]


class EquipmentStatus(models.Model):
    _name = 'equipment.status'
    _description = "Equipment Status"

    name = fields.Char('Status', required=True)
    sequence = fields.Integer('Sequence')

    _order = 'sequence'

    _sql_constraints = [('uniq_name', 'UNIQUE(name)', "Status should be Unique")]


class EquipmentPropertyValue(models.Model):
    _name = 'equipment.property.value'
    _description = "Equipment Category Property"

    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment", ondelete='cascade')
    property_id = fields.Many2one('equipment.category.property', "Property")
    property_value = fields.Char('Value', required=True)

    _sql_constraints = [('uniq_name', 'UNIQUE(equipment_id,property_id)', "Property Should be Unique")]


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    def _get_default_status(self):
        _status = self.env['equipment.status'].search([], order='sequence', limit=1)
        return _status

    @api.multi
    def _get_ip_primary(self):
        _ip_id = self.env.ref('cicon_equipment.equipment_default_property_ip').id
        for rec in self:
            if rec.property_value_ids:
                _ip_prop = rec.property_value_ids.filtered(lambda a: a.property_id.id == _ip_id).property_value or ''
                rec.primary_ip = _ip_prop

    primary_ip = fields.Char(string="IP Address(Primary)",compute=_get_ip_primary)
    internal_ref = fields.Char('Internal Ref', default='New', copy=False)
    property_ids = fields.Many2many(related='category_id.property_ids', store=False, string="Properties")
    property_value_ids = fields.One2many('equipment.property.value', 'equipment_id', string="Property Values")
    status_id = fields.Many2one('equipment.status', string='Status', track_visibility='onchange', default=_get_default_status)
    connected_to_equip_ids = fields.Many2many('maintenance.equipment', 'equipment_equip_rel', 'con_from_equip_id'
                                        ,'con_to_equip_id', string="Connected to")
    connected_from_equip_ids = fields.Many2many('maintenance.equipment', 'equipment_equip_rel', 'con_to_equip_id'
                                              , 'con_from_equip_id', string="Connected from ", readonly=True)
    pm_note = fields.Text('PM Notes')

    @api.model
    def create(self, vals):
        if vals.get('internal_ref', 'New') == 'New':
            vals['internal_ref'] = self.env['ir.sequence'].next_by_code('cicon.equip.internal.seq') or '/'
        return super(MaintenanceEquipment, self).create(vals)

      #_sql_constraints = [('UniqueAsset', 'UNIQUE(asset_code)', 'Asset Name Should be Unique !')]

    def _create_new_request(self, date):
        # Override to add company id as per equipment
        self.ensure_one()
        self.env['maintenance.request'].create({
            'name': 'PM-%s' % self.name,
            'request_date': date,
            'schedule_date': date,
            'category_id': self.category_id.id,
            'equipment_id': self.id,
            'maintenance_type': 'preventive',
            'owner_user_id': self.owner_user_id.id,
            'user_id': self.technician_user_id.id,
            'maintenance_team_id': self.maintenance_team_id.id,
            'duration': self.maintenance_duration,
            'company_id': self.company_id.id,
            'description': self.pm_note
        })


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    property_ids = fields.Many2many('equipment.category.property', 'hr_equipment_categ_property_rel',
                                    'category_id', "property_id", string="Properties")


