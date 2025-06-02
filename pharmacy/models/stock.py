from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Stock(models.Model):
    _name = 'pharmacy.stock'
    _description = 'Stock de médicament'

    name = fields.Char(string='Référence', 
                      readonly=True, default=lambda self: _('New'))
    medicine_id = fields.Many2one('pharmacy.medicine', string='Médicament')
    quantity = fields.Float(string='Quantité', required=True)
    expiry_date = fields.Date(string='Date de péremption')
    reorder_point = fields.Float(string='Seuil de réapprovisionnement', required=True)
    reorder_days = fields.Integer(string='Délai de réapprovisionnement (jours)', required=True)
    next_availability_date = fields.Date(
        string='Prochaine disponibilité',
        compute='_compute_next_availability_date',
        store=True
    )
    state = fields.Selection([
        ('available', 'Disponible'),
        ('low', 'Stock faible'),
        ('out', 'Rupture de stock'),
        ('reorder', 'En réapprovisionnement')
    ], string='État', compute='_compute_state', store=True)

    _sql_constraints = [
        ('medicine_pharmacy_uniq', 'unique(medicine_id, pharmacy_id)',
         'Un médicament ne peut avoir qu\'un seul stock par pharmacie !')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('pharmacy.stock') or _('New')
        return super().create(vals_list)

    @api.depends('quantity', 'reorder_point')
    def _compute_state(self):
        for stock in self:
            if stock.quantity <= 0:
                stock.state = 'out'
            elif stock.quantity <= stock.reorder_point:
                stock.state = 'low'
            else:
                stock.state = 'available'

    @api.depends('state', 'reorder_days')
    def _compute_next_availability_date(self):
        for stock in self:
            if stock.state in ['out', 'low']:
                stock.next_availability_date = fields.Date.today() + timedelta(days=stock.reorder_days)
            else:
                stock.next_availability_date = False

    @api.constrains('quantity', 'reorder_point')
    def _check_positive_values(self):
        for stock in self:
            if stock.quantity < 0:
                raise ValidationError(_("La quantité ne peut pas être négative !"))
            if stock.reorder_point < 0:
                raise ValidationError(_("Le seuil de réapprovisionnement ne peut pas être négatif !"))

    def action_reorder(self):
        """Action pour déclencher le réapprovisionnement"""
        for stock in self:
            if stock.state in ['out', 'low']:
                stock.state = 'reorder'
                