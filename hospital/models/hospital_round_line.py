from odoo import models, fields, api

class HospitalRoundLine(models.Model):
    _name = 'hospital.round.line'
    _description = 'Ligne de ronde infirmière'

    round_id = fields.Many2one('hospital.round', string="Ronde", required=True, ondelete="cascade")
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    state = fields.Selection([
        ('stable', 'Stable'),
        ('hospitalize', 'À hospitaliser'),
        ('pending', 'À reprogrammer')
    ], string='État constaté', required=True)

    description = fields.Text(string='Observation')
    is_follow_up_needed = fields.Boolean(string="Reprogrammer une ronde ?", default=False)
    next_round_date = fields.Date(string="Prochaine ronde")

    @api.onchange('state')
    def _onchange_state(self):
        for rec in self:
            if rec.patient_id:
                if rec.state == 'stable':
                    rec.patient_id.state = 'released'
                    rec.patient_id.is_retained = False
                else:
                    rec.patient_id.state = 'treatment'
                    rec.patient_id.is_retained = True
