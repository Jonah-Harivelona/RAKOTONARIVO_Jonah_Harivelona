from odoo import fields, models

class HospitalStaffInfirmier(models.Model):
    _name = "hospital.staff.infirmier"

    name = fields.Char(string="Nom")