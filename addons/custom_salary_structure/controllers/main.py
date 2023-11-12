# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo.addons.mail.controllers.main import MailController
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError

_logger = logging.getLogger(__name__)


class CustomSalaryController(http.Controller):
    # GET http requests
    @http.route('/custom_salary/<int:salary_struct_id>', type='http', auth='public', website=True, csrf=False, methods=['GET'])
    def send_custom_salary(self, salary_struct_id=None, **kwargs):
        if not salary_struct_id or salary_struct_id < 0:
            raise UserError('Invalid URL, please Contact your sender and try again.')

        try:
            salary_structure = request.env['contract.salary.structure'].browse(salary_struct_id)
            employee_id = salary_structure.salary_contract_id.employee_id

            if not salary_structure:
                raise UserError('Record is not found, please Contact your sender and try again.')

            editable_rules = salary_structure.salary_rule_ids.filtered(lambda x: x.is_editable)
            basic_rule = salary_structure.salary_rule_ids.filtered(lambda x: x.is_basic)

            total_amount = sum(editable_rules.mapped('amount')) + basic_rule.amount
            editable_rules_dict = (editable_rules.read(['name', 'amount', 'rule_type']))
            base_record_val = basic_rule.read(['amount'])[0]
            return request.render('custom_salary_structure.custom_salary_template',
                                  {
                                      'salary_structure': salary_structure,
                                      'editable_rules_dict': editable_rules_dict,
                                      'base_record_val': base_record_val,
                                      'gross_total': {'amount': total_amount},
                                      'employee': {'name': employee_id.name}
                                  })
        except Exception as e:
            raise UserError(f"Unexpected error: {e}")

    # POST json requests
    @http.route('/custom_salary_structure/save_changes', type='json', auth="public", website=True, csrf=False, methods=['POST'])
    def save_changes(self, result_from_js=None, **kwargs):
        json_data = request.jsonrequest
        records_data_to_update = [(int(key), val) for key, val in json_data.get('result_from_js').items()]

        # Update records
        try:
            for data in records_data_to_update:
                request.env['contract.salary.rule'].browse(data[0]).write({'employee_amount': data[1]})
            return {'message': 'Updated successfully.', 'success': True}
        except Exception as e:
            raise UserError(f"Unexpected error: {e}")


