from odoo import fields, models

class HospitalMedicament(models.Model):
    _name = "hospital.medicament"
    _description = "Medicament"

    name = fields.Char(string="Nom", required=True)
    medicament_description = fields.Text(string="Description")
    date_manufacturer = fields.Date(string="Date de fab")
    date_peremptory = fields.Date(string="Date de péremption")