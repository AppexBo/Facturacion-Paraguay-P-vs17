# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)



class PosOrder(models.Model):
    _inherit = ['pos.order']

    def get_py_payment_type(self):
        if self.payment_ids:
            pos_payment_id : models.Model = self.payment_ids[0].payment_method_id.l10n_py_payment_type_id
            if pos_payment_id:
                return pos_payment_id.id
        raise UserError('No se encontro un tipo de pago (PY)')
    
    def get_py_payments_type(self):
        if self.payment_ids:
            list_payment = []
            for payment in self.payment_ids:
                list_payment.append(
                    (
                        0, 
                        0, {
                            'l10n_py_payment_type_id': payment.payment_method_id.l10n_py_payment_type_id.id, 
                            'currency_id' : payment.currency_id.id,
                            'amount': payment.amount,
                            #'currency_rate'
                        }
                    )
                )
            return list_payment
        raise UserError('No se encontro un tipo de pago (PY)')
        
    def _prepare_invoice_vals(self):
        vals = super(PosOrder, self)._prepare_invoice_vals()
        if self.config_id.l10n_py_presence_indicator_id:
            vals['l10n_py_presence_indicator_id'] = self.config_id.l10n_py_presence_indicator_id.id
            vals['l10n_py_payment_type_id'] = self.get_py_payment_type()
            vals['l10n_py_payments_ids'] = self.get_py_payments_type()
            
        else:
            raise UserError('No se encontro una configuracion para el tipo de presencia clientes en punto de venta.')
        return vals