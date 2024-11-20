# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import base64
import requests
from requests.auth import HTTPBasicAuth
import json

import logging
_logger = logging.getLogger(__name__)



class L10nPySend(models.Model):
    
    _inherit = ['account.move']
    
    def to_base64(self):
        if self.xml_str_format:
            text_bytes = str(self.xml_str_format).encode('utf-8')
            text_base64 = base64.b64encode(text_bytes)
            self.write(
                {
                    'format_base64_xml' : text_base64,
                    'py_file_content' : text_base64,
                }
            )
        else:
            raise UserError('No se genero una estructura XML')
        
    def get_header(self):
        sync_point_id = self.company_id.get_sync_point_id()  # SyncPointId proporcionado
        
        api_key = self.company_id.get_api_key()  # ApiKey proporcionado
        #ruc = "88888888"  # RUC de la empresa

        # Generar el valor de autenticación
        auth_value = f"{sync_point_id}:{api_key}" #:{ruc}"

        return {
            "Authorization": f"Basic {auth_value}",
            "Content-Type": "application/json"
        }

        
    def py_document_register(self):

        headers = self.get_header()


        endpoint =  self.env['l10n.py.endpoint'].search(
            [
                ('operation_type','=','send'),
                ('method','=','POST')
            ]
        ) #"https://api-sandbox.hermesweb.net/api/Document/SendDocumentToAuthority"
        if endpoint:
            url = endpoint.url
            data = {
                "mapping": self.company_id.get_py_mapping(),
                "sign": "true",
                "defaultCertificate": "false",
                "async": "true" if self.company_id.test_environment else 'false',
                "fileContent": self.format_base64_xml
            }

            _logger.info(f"DATA: {data}")

            try:
                response = requests.post(url, json=data, headers=headers)
                _logger.info(response.status_code)
                if response.status_code == 200:
                    response_json = response.json()
                    _logger.info(response_json)
                    self.write({'l10n_py_response' : response_json})
                    self.process_response(response_json)
                else:
                    _logger.info('Error en la autenticación o envío:')
                    _logger.info(response.status_code)
                    _logger.info(response.text)
            except requests.exceptions.RequestException as e:
                _logger.info("Error al conectar con el servicio:")
                _logger.info(e)
                


    def process_response(self, response : dict):
        
        try:
            response = json.loads(response)
            res_data = {}
            # res_data['l10n_py_response_Success'] = response.get('Success', False)

            # self.write(res_data)
            # 
            extra_info = ''
            for key, value in response.items():
                _field = f"l10n_py_response_{key}"
                _field_value = getattr(self,_field,None)
                if _field_value != None:
                    res_data[_field] = value or False
                else:
                    extra_info += f'No se encontro el campo: {_field} = {value} |'
            if res_data:
                self.write(res_data)
            if extra_info:
                self.write(
                    {
                        'l10n_py_response_extra_info' : extra_info,
                        'l10n_py_transaction' : not self.l10n_py_response_ErrorException,
                        'edi_py_state': 'sent' if self.l10n_py_response_Code == 0 else 'observed'
                    }
                )
            
                
        except Exception as e:
            _logger.info(f"Error al procesar respuesta: {e}")


    """
        {
            "":false,
            "":"00000000-0000-0000-0000-000000000000",
            "":"01801025443001001000000322024111218961756309",
            "":null,
            "Messages":null,
            "ResponseValue":"",
            "Extra":null,
            "":99,
            "":"Error de validación.",
            "ErrorException":"The 'http://ekuatia.set.gov.py/sifen/xsd:dBasGravIVA' element is invalid - The value '0.9090909090909091' is invalid according to its datatype 'http://ekuatia.set.gov.py/sifen/xsd:tMontoBase' - The FractionDigits constraint failed.",
            "Folio":0
        }
    """


    def action_resend_invoice(self):
        self.button_draft()
        self.action_post()

    def action_py_request_document(self):
        pass

    def get_request_pdf(self):
        sync_point_id = '9d978e86-b8a0-43e3-b430-11acc0a6d1ae' #self.company_id.get_sync_point_id()  # SyncPointId proporcionado
        
        api_key = 'fusnchwsaupnwfi'#self.company_id.get_api_key()  # ApiKey proporcionado
        #ruc = "88888888"  # RUC de la empresa

        # Generar el valor de autenticación
        auth_value = f"{sync_point_id}:{api_key}" #:{ruc}"

        header = {
            "Authorization": f"Basic {auth_value}",
            "Content-Type": "application/json"
        }

        endpoint =  self.env['l10n.py.endpoint'].search(
            [
                ('name','=','Descarga PDF'),
                ('method','=','GET')
            ]
        )
        if endpoint:
            URL = endpoint.url
            URL += self.l10n_py_response_CountryDocumentId
            _logger.info(self.l10n_py_response_CountryDocumentId)

            try:
                response = requests.get(URL, headers=header)

                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    _logger.info('INFORMACION')
                    res : dict = response.json()
                    _logger.info(f"{res}")
                    documentBase64 = res.get('Base64Content', False)
                    return documentBase64
                else:
                    _logger.info(f"Error en la autenticación o consulta: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                _logger.info(f"Error al conectar con el servicio: {e}")
                
