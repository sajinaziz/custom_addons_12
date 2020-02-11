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
        _equips = self.env['maintenance.equipment'].search([])
        for rec in self:
            _eq = _equips.sudo().filtered(lambda a: a.primary_ip).filtered(lambda r: rec.name in r.primary_ip.split(','))
            if len(_eq) == 1:
                rec.equipment_id = _eq.id
            else:
                rec.equip_ids = _eq._ids

    @api.multi
    def multi_equipment(self):
        for rec in self:
            if rec.equip_ids:
                rec.equip_count = len(rec.equip_ids)
                rec.error_msg = "Multiple Equipments found !"

    equipment_ip_id = fields.Many2one('cicon.equipment.ip', "IP")
    name = fields.Char(string="IP Address", required=True)
    equipment_id = fields.Many2one('maintenance.equipment', compute=find_equipment, store=False, string="Equipment" )
    equip_ids = fields.Many2many('maintenance.equipment', compute=find_equipment, string="Multi Equipments",
                                 store=False)
    category_id = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id',
                                 store=False, string="Category")
    status_id = fields.Many2one('equipment.status', string='Status', related='equipment_id.status_id')
    ip_assign_type = fields.Selection(selection=_IP_ASSIGN_TYPE, string="IP Assign Type")
    error_msg = fields.Char(string="Error Message !", compute=multi_equipment, store=False)
    equip_count = fields.Integer(compute=multi_equipment, string="Equipment Count", store=False)
    note = fields.Char("Note")






