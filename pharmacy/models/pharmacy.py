from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class Pharmacy(models.Model):
    _name = 'pharmacy.pharmacy'
    _description = 'Pharmacie' 
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom de la pharmacie', required=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True)
    active = fields.Boolean(default=True)
    medicine_ids = fields.One2many('pharmacy.medicine', 'pharmacy_id', string='Médicaments')
    order_ids = fields.One2many('pharmacy.order', 'pharmacy_id', string='Commandes')
    # stock_ids = fields.One2many('pharmacy.stock', 'pharmacy_id', string='Stocks')
    reorder_delay = fields.Integer(string='Délai de réapprovisionnement (jours)', default=7,
                                 help="Nombre de jours avant qu'un médicament soit à nouveau disponible")
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Le code de la pharmacie doit être unique!')
    ]

    @api.depends('medicine_ids')
    def _compute_medicine_count(self):
        for pharmacy in self:
            pharmacy.medicine_count = len(pharmacy.medicine_ids)
            # Calculer les stocks faibles et ruptures via les médicaments
            low_stock = self.env['pharmacy.medicine'].search_count([
                ('pharmacy_id', '=', pharmacy.id),
                ('state', '=', 'low')
            ])
            out_stock = self.env['pharmacy.medicine'].search_count([
                ('pharmacy_id', '=', pharmacy.id),
                ('state', '=', 'out')
            ])
            pharmacy.low_stock_count = low_stock
            pharmacy.out_of_stock_count = out_stock

    medicine_count = fields.Integer(compute='_compute_medicine_count', string='Nombre de médicaments')
    low_stock_count = fields.Integer(compute='_compute_medicine_count', string='Médicaments en stock faible')
    out_of_stock_count = fields.Integer(compute='_compute_medicine_count', string='Médicaments en rupture')

    def action_view_medicines(self):
        return {
            'name': _('Médicaments'),
            'type': 'ir.actions.act_window',
            'res_model': 'pharmacy.medicine',
            'view_mode': 'list,form',
            'domain': [('pharmacy_id', '=', self.id)],
        }

    def action_view_orders(self):
        return {
            'name': _('Commandes'),
            'type': 'ir.actions.act_window',
            'res_model': 'pharmacy.order',
            'view_mode': 'list,form',
            'domain': [('pharmacy_id', '=', self.id)],
        }

    @api.model
    def _cron_check_stock_levels(self):
        """Vérifier les niveaux de stock et mettre à jour les états"""
        medicines = self.search([('active', '=', True)])
        for medicine in medicines:
            medicine._onchange_stock_quantity()

class MedicineCategory(models.Model):
    _name = 'pharmacy.category'
    _description = 'Catégorie de médicament'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('pharmacy.category', string='Catégorie parente')
    child_ids = fields.One2many('pharmacy.category', 'parent_id', string='Sous-catégories')
    medicine_count = fields.Integer(compute='_compute_medicine_count', string='Nombre de médicaments')

    @api.depends('child_ids')
    def _compute_medicine_count(self):
        for category in self:
            category.medicine_count = self.env['pharmacy.medicine'].search_count([
                ('category_id', '=', category.id)
            ])

class Medicine(models.Model):
    _name = 'pharmacy.medicine'
    _description = 'Médicament'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='Code', required=True)
    pharmacy_id = fields.Many2one('pharmacy.pharmacy', string='Pharmacie', required=True)
    category_id = fields.Many2one('pharmacy.category', string='Catégorie', required=True)
    manufacturer = fields.Char(string='Fabricant')
    description = fields.Text(string='Description')
    price = fields.Float(string='Prix', required=True)
    stock_quantity = fields.Float(string='Quantité en stock', default=0)
    min_stock = fields.Float(string='Stock minimum', default=10)
    reorder_point = fields.Float(string='Point de réapprovisionnement', default=20)
    equivalent_medicine_ids = fields.Many2many('pharmacy.medicine', 'medicine_equivalents_rel',
                                             'medicine_id', 'equivalent_id',
                                             string='Médicaments équivalents')
    state = fields.Selection([
        ('available', 'Disponible'),
        ('low', 'Stock faible'),
        ('out', 'Rupture de stock'),
        ('reorder', 'En réapprovisionnement')
    ], string='État', default='available', tracking=True)
    next_available_date = fields.Date(string='Date de disponibilité')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Société', 
                                default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    _sql_constraints = [
        ('code_pharmacy_uniq', 'unique(code, pharmacy_id)', 
         'Le code du médicament doit être unique par pharmacie!')
    ]

    @api.onchange('stock_quantity')
    def _onchange_stock_quantity(self):
        for medicine in self:
            if medicine.stock_quantity <= 0:
                medicine.state = 'out'
                medicine.next_available_date = fields.Date.today() + timedelta(days=medicine.pharmacy_id.reorder_delay)
            elif medicine.stock_quantity < medicine.min_stock:
                medicine.state = 'low'
            else:
                medicine.state = 'available'
                medicine.next_available_date = False

    def action_reorder(self):
        """Marquer le médicament comme en réapprovisionnement"""
        self.write({
            'state': 'reorder',
            'next_available_date': fields.Date.today() + timedelta(days=self.pharmacy_id.reorder_delay)
        })

    @api.model
    def _cron_check_stock_levels(self):
        """Vérifier les niveaux de stock et mettre à jour les états"""
        medicines = self.search([('active', '=', True)])
        for medicine in medicines:
            medicine._onchange_stock_quantity() 