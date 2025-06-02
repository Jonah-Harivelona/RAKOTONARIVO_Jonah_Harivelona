from odoo import fields, models, api

class HospitalConsultation(models.Model):
    _name = "hospital.consultation"
    _description = "Consultation médicale"

    name = fields.Char(string="Référence", required=True, default="Nouvelle")
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.staff.doctor', string="Médecin", required=True)
    consultation_date = fields.Datetime(string="Date", default=fields.Datetime.now)
    ligne_consultation_ids = fields.One2many('hospital.consultation.line', 'consultation_id', string="Médicaments prescrits")
    symptom_ids = fields.Many2many('hospital.symptom', string="Symptômes observés")
    montant_total = fields.Float(string="Montant total (ar)", compute="_compute_total")
    
    # Nouveaux champs pour la fiche patient
    advice = fields.Text(string="Conseils médicaux", help="Conseils donnés au patient")
    diagnosis = fields.Text(string="Diagnostic", help="Diagnostic du médecin")
    final_action = fields.Selection([
        ('home', "Rentre à la maison"),
        ('hospital', "Hospitalisation"),
        ('follow_up', "Suivi médical"),
    ], string="Action finale")
    similar_cases = fields.Many2many('hospital.consultation', 
                                   compute='_compute_similar_cases',
                                   string="Cas similaires",
                                   help="Consultations similaires basées sur les symptômes"
                                   )
    recommended_medicaments = fields.Many2many('hospital.medicament',
                                             compute='_compute_recommended_medicaments',
                                             string="Médicaments recommandés",
                                             help="Médicaments recommandés basés sur les symptômes"
                                             )
    days_to_stay = fields.Integer(string="Jours d'hospitalisation", help="Nombre de jours si hospitalisation requise"
                                 )
    follow_up_date = fields.Date(string="Date de suivi",
                                help="Date du prochain rendez-vous si suivi requis")

    @api.depends('price_unit','quantity')
    def _compute_sub_total(self):
        for ligne in self:
            ligne.sub_total = ligne.price_unit * ligne.quantity
            
    state = fields.Selection([
        ('draft', 'Non-traitée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé')
    ], default='draft', string="État")

    @api.depends('ligne_consultation_ids.sub_total')
    def _compute_total(self):
        for record in self:
            record.montant_total = sum(ligne.sub_total for ligne in record.ligne_consultation_ids)

    @api.depends('symptom_ids')
    def _compute_similar_cases(self):
        for record in self:
            if record.symptom_ids:
                # Recherche des consultations avec des symptômes similaires
                similar_cases = self.search([
                    ('id', '!=', record.id),
                    ('symptom_ids', 'in', record.symptom_ids.ids),
                    ('state', '=', 'done')
                ], limit=5)
                record.similar_cases = similar_cases
            else:
                record.similar_cases = False

    @api.depends('symptom_ids')
    def _compute_recommended_medicaments(self):
        for record in self:
            if record.symptom_ids:
                # Recherche des médicaments recommandés pour ces symptômes
                recommended = self.env['hospital.medicament'].search([
                    ('symptom_ids', 'in', record.symptom_ids.ids)
                ])
                record.recommended_medicaments = recommended
            else:
                record.recommended_medicaments = False

    def action_print_patient_record(self):
        return self.env.ref('hospital.action_report_patient_record').report_action(self)