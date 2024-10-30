

from odoo import models, fields

class ResCity(models.Model):
    _inherit = ['res.city']
    
    
    code = fields.Char(
        string='Codigo',
    )
    