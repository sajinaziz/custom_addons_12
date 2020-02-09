from odoo import models, fields, api
from odoo.exceptions import UserError
from ipaddress import ip_address, ip_network


class CiconEquipmetIp(models.Model):
    _name = 'cicon.equipment.ip'
    _description = "Equipment IP"

    @api.multi
    def _get_ip_line_equip(self):
        for rec in self:
            rec.ip_equip_lines = rec.ip_lines.filtered(lambda e: e.equipment_id or e.equip_count > 0)

    name = fields.Char(string="Network Title", required=True)
    ip_class = fields.Char("IP Network", required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id)
    ip_lines = fields.One2many('cicon.equipment.ip.line', 'equipment_ip_id', string="IP Lines")
    ip_equip_lines = fields.One2many('cicon.equipment.ip.line', 'equipment_ip_id', compute=_get_ip_line_equip, readonly=1,
                                     string="IP Lines")

    def generate_ip_range(self):
        if len(self.ip_lines) == 0:
            try:
                _ips = list(ip_network(self.ip_class).hosts())
                _dic = [{'name': str(ip)} for ip in _ips]
                self.ip_lines = _dic
            except ValueError:
                raise UserError("IP Error")
        else:
            raise UserError("IP Range exists !")

    _sql_constraints = [('uniq_name', 'UNIQUE(name)', "Title Should be same"),
                        ('uniq_ip_class', 'UNIQUE(ip_class,company_id)', "IP Network should be unique in Company !")]


class CiconEquipmentIpLine(models.Model):
    _name = 'cicon.equipment.ip.line'
    _description = "Equipment IP Lines"

    _IP_ASSIGN_TYPE = [('static', 'Static'), ('dhcp', 'DHCP'),
                                              ('dchp_reserved', 'DHCP Reserved')]

    @api.multi
    def find_equipment(self):
        _ip_id = self.env.ref('cicon_equipment.equipment_default_property_ip').id
        _equips = self.env['equipment.property.value'].search([('property_id', '=', _ip_id)]).mapped('equipment_id')
        for rec in self:
            _eq = _equips.sudo().filtered(lambda r: r.primary_ip == rec.name and r.company_id == self.env.user.company_id)
            if len(_eq) == 1:
                rec.equipment_id = _eq.id
            else:
                rec.error_msg = "Multiple Equipment assigned!"
                rec.equip_ids = _eq._ids
                rec.equip_count = len(_eq)

    equipment_ip_id = fields.Many2one('cicon.equipment.ip', "IP")
    name = fields.Char(string="IP Address", required=True)
    equipment_id = fields.Many2one('maintenance.equipment', compute=find_equipment, store=False, string="Equipment")
    company_id = fields.Many2one('res.company', related='equipment_id.company_id', store=False, string="Company")
    status_id = fields.Many2one('equipment.status', string='Status', related='equipment_id.status_id')
    ip_assign_type = fields.Selection(selection=_IP_ASSIGN_TYPE, string="IP Assign Type")
    error_msg = fields.Char(string="Error Message !", compute=find_equipment, store=False)
    equip_ids = fields.Many2many('maintenance.equipment', compute=find_equipment, string="Multi Equipments")
    equip_count = fields.Integer(compute=find_equipment, string="Equipment Count")
    note = fields.Char("Note")






