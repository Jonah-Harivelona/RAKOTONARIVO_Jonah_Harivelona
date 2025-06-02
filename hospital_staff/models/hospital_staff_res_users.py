from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_infirmiere = fields.Boolean(string="Est infirmière ?", default=False)