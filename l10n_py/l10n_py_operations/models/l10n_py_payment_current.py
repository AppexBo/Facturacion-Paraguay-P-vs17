# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError

class L10nPyPaymentCurrent(models.Model):
    _inherit = ['l10n.py.payment.currency']
    
    def get_E606(self):
        if self.l10n_py_payment_type_id:
            if self.l10n_py_payment_type_id.code not in ['1','3','4','5']:
                raise UserError(f'EL metodo de pago: {self.l10n_py_payment_type_id.name}, no esta disponible')
            return self.l10n_py_payment_type_id.code
        raise UserError('Por favor establezca un metodo de pago')
    

    def get_E607(self):
        if self.l10n_py_payment_type_id:
            return self.l10n_py_payment_type_id.description
        raise UserError('Por favor establezca un metodo de pago')
    
    def get_E608(self):
        return self.amount
    
    
    def get_E609(self):
        return self.currency_id.getCode()
    
    def get_E610(self):
        return self.currency_id.getdDescription()
    
    
    def get_E611(self):
        return self.currency_id.get_py_rate()