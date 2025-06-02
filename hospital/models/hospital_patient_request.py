from odoo import models, fields, api

class HospitalPatient(models.Model):
    _name = 'hospital.patient.request'
    _description = "Demande du consultation"

    doctor_id = fields.Many2one('hospital.staff.doctor', string='Médecin demandé', required=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required = True)
    symptoms = fields.Text(string="Symptômes")
    state = fields.Selection([
        ('submitted', 'Envoyée'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
    ], string='État médical', default='submitted')

    # status = fields.Selection([
    #     ('waiting', 'En attente'),
    #     ('treatment', 'À hospitaliser'),
    #     ('released', 'Libre de partir'),
    # ], string="Décision", default='waiting')
    
    is_retained = fields.Boolean(string="Retenir sur place ?", default=False)

    def action_submit(self):
        for record in self:
            record.state = 'submitted'
        return True

    # @api.onchange('status', 'is_retained')
    # def _onchange_update_patient(self):
    #     if self.patient_id:
    #     # on ne met à jour le state du patient que si c'est une valeur valide
    #      if self.status in ['treatment', 'released']:
    #         self.patient_id.state = self.state
    #         self.patient_id.is_retained = self.is_retained


    # def action_validate_request(self):
    #      for rec in self:
    #         if rec.patient_id:
    #         # Traduction des états de la demande vers les états du patient
    #           mapped_state = {
    #             'submitted': 'treatment',
    #             'accepted': 'recovery',
    #             'rejected': 'released',
    #           }.get(rec.state)

    #           if mapped_state:
    #                 rec.patient_id.state = mapped_state
    #           else:
    #                 rec.patient_id.state = 'treatment'
    #           rec.patient_id.is_retained = rec.is_retained
