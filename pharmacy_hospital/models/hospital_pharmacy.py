from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class HospitalPharmacyOrder(models.Model):
    _name = 'hospital.pharmacy.order'
    _description = 'Commande de médicaments de l\'hôpital'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc'

    name = fields.Char(string='Référence', required=True, copy=False, 
                      readonly=True, default=lambda self: _('New'))
    hospital_id = fields.Many2one('hospital.hospital', string='Hôpital', required=True, tracking=True)
    pharmacy_id = fields.Many2one('pharmacy.pharmacy', string='Pharmacie', required=True, tracking=True)
    date_order = fields.Datetime(string='Date de commande', required=True, default=fields.Datetime.now)
    order_line_ids = fields.One2many('hospital.pharmacy.order.line', 'order_id', string='Lignes de commande')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('sent', 'Envoyée'),
        ('confirmed', 'Confirmée par la pharmacie'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée')
    ], string='État', default='draft', tracking=True)
    amount_total = fields.Monetary(compute='_compute_amount_total', string='Total', store=True)
    company_id = fields.Many2one('res.company', string='Société', 
                                default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    notes = fields.Text(string='Notes')
    expected_delivery_date = fields.Date(string='Date de livraison prévue', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.pharmacy.order') or _('New')
        return super().create(vals)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(line.price_subtotal for line in order.order_line_ids)

    def action_send(self):
        """Envoyer la commande à la pharmacie"""
        self.write({'state': 'sent'})
        
        pharmacy_order = self.env['pharmacy.order'].create({
            'name': self.name,
            'pharmacy_id': self.pharmacy_id.id,
            'partner_id': self.hospital_id.partner_id.id,
            'date_order': self.date_order,
            'order_line_ids': [(0, 0, {
                'medicine_id': line.medicine_id.id,
                'name': line.name,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
            }) for line in self.order_line_ids],
        })
        return True

    def action_confirm(self):
        """Confirmer la commande"""
        self.write({'state': 'confirmed'})

    def action_done(self):
        """Marquer la commande comme terminée"""
        self.write({'state': 'done'})

    def action_cancel(self):
        """Annuler la commande"""
        self.write({'state': 'cancelled'})

    def action_draft(self):
        """Remettre en brouillon"""
        self.write({'state': 'draft'})

    @api.model
    def _cron_check_pending_orders(self):
        """Vérifier les commandes en attente et envoyer des alertes si nécessaire"""
        pending_orders = self.search([
            ('state', 'in', ['sent', 'confirmed']),
            ('expected_delivery_date', '<', fields.Date.today())
        ])
        for order in pending_orders:
            order.message_post(
                body=_("La commande est en retard par rapport à la date de livraison prévue.")
            )

class HospitalPharmacyOrderLine(models.Model):
    _name = 'hospital.pharmacy.order.line'
    _description = 'Ligne de commande de médicaments de l\'hôpital'

    order_id = fields.Many2one('hospital.pharmacy.order', string='Commande', required=True, ondelete='cascade')
    medicine_id = fields.Many2one('pharmacy.medicine', string='Médicament', required=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(string='Quantité', required=True, default=1.0)
    price_unit = fields.Float(string='Prix unitaire', required=True)
    price_subtotal = fields.Monetary(compute='_compute_subtotal', string='Sous-total', store=True)
    currency_id = fields.Many2one(related='order_id.currency_id')
    equivalent_medicine_ids = fields.Many2many(related='medicine_id.equivalent_medicine_ids',
                                             string='Médicaments équivalents disponibles')

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

    @api.onchange('medicine_id')
    def _onchange_medicine_id(self):
        if self.medicine_id:
            self.name = self.medicine_id.name
            self.price_unit = self.medicine_id.price
            if self.medicine_id.state == 'out':
                return {
                    'warning': {
                        'title': _('Médicament non disponible'),
                        'message': _('Ce médicament n\'est pas disponible. Des médicaments équivalents sont peut-être disponibles.')
                    }
                } 