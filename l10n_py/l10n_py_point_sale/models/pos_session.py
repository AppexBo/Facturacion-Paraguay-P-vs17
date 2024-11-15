from odoo import api, fields, models


import logging
_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = 'pos.session'

    # -------------------------------------------------------------------------------------------------------------------------

    def _get_pos_ui_l10n_latam_identification_type(self, params):
        return self.env["l10n_latam.identification.type"].search_read(**params["search_params"])
    
    def _loader_params_l10n_latam_identification_type(self):
        return {'search_params': {'domain': [], 'fields': ['name']}}
    
    # -------------------------------------------------------------------------------------------------------------------------
    
    def _get_pos_ui_l10n_py_operation_type(self, params):
        return self.env['l10n.py.operation.type'].search_read(**params['search_params'])
    
    def _loader_params_l10n_py_operation_type(self):
        return {'search_params': {'domain': [], 'fields': ['name', 'code', 'description']}}
    
    # -------------------------------------------------------------------------------------------------------------------------

    def _get_pos_ui_res_city(self, params):
        return self.env['res.city'].search_read(**params['search_params'])
    
    def _loader_params_res_city(self):
        return {'search_params': {'domain': [], 'fields': ['name']}}
    
    # -------------------------------------------------------------------------------------------------------------------------
    
    def _get_pos_ui_l10n_py_locality(self, params):
        return self.env['l10n.py.locality'].search_read(**params['search_params'])
    
    def _loader_params_l10n_py_locality(self):
        return {'search_params': {'domain': [], 'fields': ['name']}}
    
    # -------------------------------------------------------------------------------------------------------------------------
    
    def _loader_params_res_partner(self):
        res = super(PosSession, self)._loader_params_res_partner()
        add_list = ["l10n_latam_identification_type_id", 'operation_type_id','distrit_id','locality_id', 'receiver_nature', 'taxpayer_type', 'house_number']
        res['search_params']['fields'] += add_list
        _logger.info(f"Campos agregados al partner POS: {add_list}")
        return res

    @api.model
    def _pos_ui_models_to_load(self):
        res = super(PosSession, self)._pos_ui_models_to_load()
        models_to_load = [
            'l10n.py.operation.type',
            'l10n_latam.identification.type',
            'res.city',
            'l10n.py.locality'
        ]
        res+= models_to_load
        _logger.info(f"Modelos agregados al POS: {models_to_load}")
        return res
    
        
    #def _loader_params_l10n_bo_card(self):
    #    return {
    #        'search_params': {'fields': ['name','card'],},}

    #def _get_pos_ui_l10n_bo_card(self, params):
    #    return self.env['l10n.bo.card'].search_read(**params['search_params'])
    


    # def _loader_params_pos_payment(self):
    #     return {'search_params': {'domain': [],'fields': ['card','order']}}

    # def _get_pos_ui_pos_payment(self, params):
    #     return self.env['pos.payment'].search_read(**params['search_params'])