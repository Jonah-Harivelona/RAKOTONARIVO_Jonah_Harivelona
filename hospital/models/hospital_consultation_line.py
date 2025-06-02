from odoo import fields, models, api

class HospitalConsultationLine(models.Model):
    _name = "hospital.consultation.line"
    _description = "ligne de consultation"

    ligne_medicament_id = fields.Many2one("hospital.medicament", string="Médicaments") #Chaque ligne de consultation est liée a un seul médicament
    consultation_id = fields.Many2one("hospital.consultation", string="Consultation")
    price_unit = fields.Float(string="Prix unitaire")
    quantity = fields.Integer(string="Quantité")
    sub_total = fields.Float(compute = '_compute_sub_total', string="Sub_total")

    @api.depends('price_unit','quantity')
    def _compute_sub_total(self):
        for ligne in self:
            ligne.sub_total = ligne.price_unit * ligne.quantity

