# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.fields import Date
from odoo.tests import common
from odoo.exceptions import UserError


class TestHrPayrollRule(common.TransactionCase):
    def setUp(self):
        super(TestHrPayrollRule, self).setUp()
        self.hr_salary_rule = self.env['hr.salary.rule']

    def test_onchange_is_basic(self):
        rule = self.hr_salary_rule.create({
            'name': 'Test Rule',
            'is_basic': False,
            'rule_type': 'deduction',
            'appear_on_contract_structure': True,
        })

        rule._onchange_is_basic()

        self.assertEqual(rule.rule_type, 'other', "The rule_type should be 'other' when is_basic is True")

        rule.is_basic = True

        rule._onchange_is_basic()

        self.assertEqual(rule.rule_type, 'other', "The rule_type should be 'other' when is_basic is True")

        rule.is_basic = False

        rule._onchange_is_basic()

        self.assertEqual(rule.rule_type, 'other', "The rule_type should be 'other' when is_basic is False")


class TestHrContract(common.TransactionCase):
    def setUp(self):
        super(TestHrContract, self).setUp()
        self.hr_contract = self.env['hr.contract']
        self.contract_salary_structure = self.env['contract.salary.structure']
        self.mail_template = self.env.ref('custom_salary_structure.custom_salary_mail_template')

    def test_create_with_struct_id(self):
        struct_id = self.env['hr.payroll.structure'].create({
            'name': 'Test Structure',
            'rule_ids': [(0, 0, {
                'name': 'Test Rule',
                'amount_fix': 1000,
                'is_editable': True,
                'rule_type': 'deduction',
                'is_basic': False,
            })],
        })

        contract = self.hr_contract.create({
            'name': 'Test Contract',
            'wage': 5000,
            'struct_id': struct_id.id,
        })

        # Check if a salary structure is created for the contract
        self.assertTrue(contract.salary_structure_ids, "A salary structure should be created for the contract")

        # Check the values of the created salary structure
        salary_structure = contract.salary_structure_ids
        self.assertEqual(salary_structure.name, 'Test Contract Custom Salary Structure', "Incorrect salary structure name")
        self.assertEqual(len(salary_structure.salary_rule_ids), 1, "Incorrect number of salary rules")

    def test_create_without_struct_id(self):
        # Create a contract without a structure
        contract = self.hr_contract.create({
            'name': 'Test Contract',
            'wage': 5000,
        })

        # Check if no salary structure is created for the contract
        self.assertFalse(contract.salary_structure_ids, "No salary structure should be created for the contract")

    """ Email Testing """
    def test_send_email_no_salary_structure(self):
        # Create a contract without a salary structure
        contract = self.hr_contract.create({
            'name': 'Test Contract',
            'wage': 5000,
        })

        with self.assertRaises(UserError):
            contract.send_email()

    def test_send_email_with_salary_structure(self):
        contract = self.hr_contract.create({
            'name': 'Test Contract',
            'wage': 5000,
        })
        salary_structure = self.contract_salary_structure.create({
            'name': 'Test Salary Structure',
            'salary_contract_id': contract.id,
        })
        contract.salary_structure_ids = salary_structure

        contract.send_email()

