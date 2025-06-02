from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class PharmacyOrder(models.Model):
    _name = 'pharmacy.order'
    _description = 'Commande de Pharmacie'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc, id desc'

    name = fields.Char(string='Référence', required=True, copy=False, 
                      readonly=True, default=lambda self: _('New'))
    pharmacy_id = fields.Many2one('pharmacy.pharmacy', string='Pharmacie', 
                                 required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True, 
                                tracking=True)
    date_order = fields.Datetime(string='Date de commande', required=True, 
                                default=fields.Datetime.now, tracking=True)
    company_id = fields.Many2one('res.company', string='Société', 
                                default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', 
                                 string='Devise')
    
    order_line_ids = fields.One2many('pharmacy.order.line', 'order_id', 
                                    string='Lignes de commande')
    amount_total = fields.Monetary(string='Total', compute='_compute_amount_total', 
                                 store=True)
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée')
    ], string='État', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('pharmacy.order') or _('New')
        return super().create(vals_list)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('price_subtotal'))

    def action_confirm(self):
        for order in self:
            if not order.order_line_ids:
                raise UserError(_('Vous ne pouvez pas confirmer une commande sans ligne.'))
            order.state = 'confirmed'

    def action_done(self):
        for order in self:
            if order.state != 'confirmed':
                raise UserError(_('Seules les commandes confirmées peuvent être marquées comme terminées.'))
            order.state = 'done'

    def action_cancel(self):
        for order in self:
            if order.state == 'done':
                raise UserError(_('Les commandes terminées ne peuvent pas être annulées.'))
            order.state = 'cancelled'

    def action_draft(self):
        for order in self:
            if order.state == 'done':
                raise UserError(_('Les commandes terminées ne peuvent pas être remises en brouillon.'))
            order.state = 'draft'

class PharmacyOrderLine(models.Model):
    _name = 'pharmacy.order.line'
    _description = 'Ligne de commande de pharmacie'

    order_id = fields.Many2one('pharmacy.order', string='Commande', required=True, 
                              ondelete='cascade')
    medicine_id = fields.Many2one('pharmacy.medicine', string='Médicament', 
                                 required=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(string='Quantité', required=True, default=1.0)
    price_unit = fields.Float(string='Prix unitaire', required=True, digits='Product Price')
    price_subtotal = fields.Monetary(string='Sous-total', compute='_compute_price_subtotal', 
                                   store=True)
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id', 
                                 string='Devise')

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

    @api.onchange('medicine_id')
    def _onchange_medicine_id(self):
        if self.medicine_id:
            self.name = self.medicine_id.name
            self.price_unit = self.medicine_id.list_price 