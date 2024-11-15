/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PartnerDetailsEdit } from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

patch(PartnerDetailsEdit.prototype, {
    setup() {
        super.setup(...arguments);
        
        this.intFields.push(
            "l10n_latam_identification_type_id", 
            "operation_type_id",
            'distrit_id',
            'locality_id',
            "receiver_nature",
            'house_number'
        );

        // Lista de opciones para receiver_nature
        this.receiverNatureOptions = [
            ['1', "(1) Contribuyente"],
            ['2', "(2) No contribuyente"]
        ];
        
        this.taxpayer_type_options = [
            ['1', "Persona Física"],
            ['2', "Persona Jurídica"]
        ];
        

        // Establecer el valor inicial si existe en el partner
        this.changes.l10n_latam_identification_type_id = this.props.partner.l10n_latam_identification_type_id && this.props.partner.l10n_latam_identification_type_id[0];
        this.changes.operation_type_id = this.props.partner.operation_type_id && this.props.partner.operation_type_id[0];
        this.changes.distrit_id = this.props.partner.distrit_id && this.props.partner.distrit_id[0];
        this.changes.locality_id = this.props.partner.locality_id && this.props.partner.locality_id[0];
        this.changes.receiver_nature = this.props.partner.receiver_nature || '';
        this.changes.taxpayer_type = this.props.partner.taxpayer_type || '';
        this.changes.house_number = this.props.partner.house_number;
    },
    saveChanges() {
        return super.saveChanges(...arguments);
    },
});
