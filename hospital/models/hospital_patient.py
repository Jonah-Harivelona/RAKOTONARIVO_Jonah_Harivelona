from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = "Patient"

    name = fields.Char(string="Nom du patient")
    is_retained = fields.Boolean(string='Retenu sur place ?', default=False)
    request_ids = fields.One2many('hospital.patient.request', 'patient_id', string="Demande de consultation")
    symptom_ids = fields.One2many('hospital.symptom','patient_id',string="Symptômes")
    doctor_id = fields.Many2one('hospital.staff.doctor', string='Médecin demandé')
    round_ids = fields.One2many('hospital.round', 'patient_id', string='Rondes')
    state = fields.Selection([
        ('treatment', 'En traitement'),
        ('recovery', 'En rémission'),
        ('released', 'Libre de partir'),
    ], string='État médical', default='treatment')
