from odoo import fields, models

class HospitalStaffDoctor(models.Model):
    _name = "hospital.staff.doctor"

    name = fields.Char(string="Nom", required=True)