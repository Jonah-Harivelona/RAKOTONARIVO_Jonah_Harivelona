from odoo import models, fields,api

class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = "Maladies"

    name = fields.Char(string="Nom", required=True)
    symptom_ids = fields.Many2many('hospital.symptom', string="Symptôme")
    disease_gravity = fields.Selection([
        ('low', 'Moins grave'),
        ('high', 'Grave'),  
    ], string="Gravité", default="low", required=True)

      # Action finale : patient à domicile ou hospitalisé
    final_action = fields.Selection([
        ('home', "Rentre à la maison"),
        ('hospital', "Hospitalisation")
    ], string="Action finale", required=True)

    # Si hospitalisation : nombre de jours
    days_to_stay = fields.Integer(
        string="Jrs d'hospitalisation"
    )

    # Il peut rentrer chez lui mais doit acheter des Médicaments ou avoir un conseil 
    needs_medicament = fields.Boolean(
        string="Médicaments prescrits"
    )
    advice = fields.Text(
        string="Conseils",
        help="Conseils à donner au patient (même si pas de médicaments)"
    )

    @api.onchange('final_action')
    def _onchange_final_action(self):
        # Si on choisit 'home', on remet à zéro 'days_to_stay'
        if self.final_action == 'home':
            self.days_to_stay = 0