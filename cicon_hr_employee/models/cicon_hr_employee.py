from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    cicon_employee_id = fields.Integer('Employee ID', size=10, help="Employee ID")

    _sql_constraints = [('unique_cicon_id', 'UNIQUE(cicon_employee_id)', 'Unique CICON ID')]

    _order = 'cicon_employee_id'

    @api.multi
    def name_get(self):
        res = []
        for r in self.read(['name', 'cicon_employee_id']):
            res.append((r['id'], '[%s] %s' % (r['cicon_employee_id'], r['name'])))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=80):
        ids = []
        if name.isdigit():
            ids = self.search([('cicon_employee_id', operator, name)])
        else:
            if args:
                ids = self.search([('name', operator, name)] + args)
            else:
                ids = self.search([('name', operator, name)])
        return ids.name_get()