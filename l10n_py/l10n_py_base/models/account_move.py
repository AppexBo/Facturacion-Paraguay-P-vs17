# -*- coding:utf-8 -*-

from odoo import api, models, fields

class AccountMove(models.Model):
    _inherit = ['account.move']
    
    
    l10n_py_invoice_sign_date = fields.Datetime(
        string='Fecha firmado (PY)'
    )

    
    l10n_py_ringing_date = fields.Date(
        string='Fecha inicio vigencia timbrado (PY)',
    )

    
    l10n_py_emision_date = fields.Datetime(
        string='Fecha emision factura (PY)',
    )
    
    
    
    l10n_py_payment_type_id = fields.Many2one(
        string='Tipo pago (PY)',
        comodel_name='l10n.py.payment.type'
    )

    l10n_py_transaction_type_id = fields.Many2one(
        string='Tipo transacccion',
        comodel_name='l10n.py.transaction.type'
    )