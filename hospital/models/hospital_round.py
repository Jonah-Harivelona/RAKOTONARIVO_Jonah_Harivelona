from odoo import models, fields, api

class HospitalRound(models.Model):
    _name = 'hospital.round'
    _description = 'Ronde infirmière'
    
    name = fields.Char(string="Titre", compute='_compute_name', store=True)
    infirmiere_id = fields.Many2one('res.users', string="Infirmière", default=lambda self: self.env.user)
    date_round = fields.Date(string="Date de la ronde", required=True)
    line_ids = fields.One2many('hospital.round.line','round_id', string="Patients à visiter")
    patient_id = fields.Many2one('hospital.patient')

    @api.depends('infirmiere_id', 'date_round')
    def _compute_name(self):
        for rec in self:
            if rec.infirmiere_id and rec.date_round:
                rec.name = f"Ronde - {rec.infirmiere_id.name} - {rec.date_round.strftime('%d/%m/%Y')}"
            else:
                rec.name = "Nouvelle ronde"

    def action_print_weekly_report(self):
        return self.env.ref('hospital.action_report_round_weekly').report_action(self)
