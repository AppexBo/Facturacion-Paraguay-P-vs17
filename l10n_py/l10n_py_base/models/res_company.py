# -*- coding:utf-8 -*-

from odoo import api, models, fields

class ResCompany(models.Model):
    
    _inherit = ['res.company']

    
    api_key = fields.Char(
        string='API Key',
    )

    
    sync_point = fields.Char(
        string='SyncPointId',
    )
    
    
    ringing_ids = fields.One2many(
        string='Lineas de timbrado',
        comodel_name='l10n.py.ringing',
        inverse_name='company_id',
    )
    
    

    
    enable_py_invoice = fields.Boolean(
        string='Habilitar facturacion paraguaya',
    )

    
    taxpayer_type = fields.Selection(
        string='Tipo de contribuyente',
        selection=[
            ('1', 'Persona Física'), 
            ('2', 'Persona Jurídica')
        ]
    )

    
    
    test_environment = fields.Boolean(
        string='Entorno de prueba',
        default=True
    )

    
    number_house = fields.Char(
        string='Numero de casa',
    )

    
    distrit_id = fields.Many2one(
        string='Distrito',
        comodel_name='res.city',
    )
    
    locality_id = fields.Many2one(
        string='Cuidad',
        comodel_name='l10n.py.locality',
    )
    
    
    document_issuer_phone_number = fields.Char(
        string='Numero de telefono emisor',
    )

    
    econonic_activity_id = fields.Many2one(
        string='Actividad economica',
        comodel_name='l10n.py.economic.activity'
    )
    
    
    

    
    
    
    
    
    def _localization_use_documents(self):
        self.ensure_one()
        return self.enable_py_invoice
    
