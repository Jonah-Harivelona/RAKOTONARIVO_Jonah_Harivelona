from odoo import models, fields

class HospitalSymptom(models.Model):
    _name = "hospital.symptom"
    _description = "Symptôme"

    name = fields.Char(required=True, string="Nom du symptôme")
    description = fields.Text(string="Description")
    disease_gravity = fields.Selection([
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
    ], string="Gravité")
    symptom_id = fields.Many2one('hospital.patient')
    patient_id = fields.Many2one('hospital.patient')