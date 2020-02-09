from odoo import models, fields, api


class WizardEquipIpAssign(models.TransientModel):
    _name = 'wizard.equip.ip.assign'
    _description = "Equipment IP Assign Wizard"

    _IP_ASSIGN_TYPE = [('static', 'Static'), ('dhcp', 'DHCP'),
                       ('dchp_reserved', 'DHCP Reserved')]

    ip_line_ids = fields.Many2many('cicon.equipment.ip.line', 'wizard_equip_ip_assign_rel', column1='ip_line_id',column2='ip_wizard_id',
                                   string="IP")
    note = fields.Char("Note")
    ip_assign_type = fields.Selection(selection=_IP_ASSIGN_TYPE, string="IP Assign Type")

    def update_ip_line(self):
        for _rec in self.ip_line_ids:
            _rec.ip_assign_type = self.ip_assign_type
            if self.note:
                _rec.note = self.note


