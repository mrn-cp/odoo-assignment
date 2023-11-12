from odoo import _, api, fields, models
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError


class HrPayrollStructure(models.Model):
    _inherit = "hr.payroll.structure"

    is_default = fields.Boolean(string='Default', default=False)


class HrPayrollRule(models.Model):
    _inherit = "hr.salary.rule"

    is_editable = fields.Boolean(string='Editable by Employee', default=False)
    is_basic = fields.Boolean('Is Basic')
    rule_type = fields.Selection([
        ('deduction', 'Deduction'),
        ('allowance', 'Allowance'),
        ('other', 'Other'),
    ], 'Rule Type', default='other', tracking=True, required=True)
    appear_on_contract_structure = fields.Boolean('Appear on Contract Structure',
                                    help='This field will responsible for creation of custom salary rule in contract.')

    @api.onchange('is_basic')
    def _onchange_is_basic(self):
        if self.is_basic:
            self.rule_type = 'other'


class HrContract(models.Model):
    _inherit = "hr.contract"

    salary_structure_ids = fields.One2many("contract.salary.structure", 'salary_contract_id', "Custom Salary Structure", copy=False)

    def send_email(self):
        if not self.salary_structure_ids:
            raise UserError('Please create Custom Salary Structure before sending an email to the employee.')
        template = self.env.ref('custom_salary_structure.custom_salary_mail_template')
        for rec in self:
            # template.send_mail(rec.id)
            template.send_mail(rec.id, force_send=True)

    @api.model
    def create(self, vals):
        res = super(HrContract, self).create(vals)
        if res.struct_id:
            salary_rule_vals = []
            salary_rules = res.struct_id.rule_ids
            for rule in salary_rules:
                salary_rule_vals.append((0, 0, {
                    'name': rule.name,
                    'amount': rule.amount_fix,
                    'employee_amount': 0,
                    'is_editable': rule.is_editable,
                    'rule_type': rule.rule_type,
                    'is_basic': rule.is_basic
                }))

            record = self.env['contract.salary.structure'].create({
                'name': '%s Custom Salary Structure' % res.employee_id.name,
                'salary_contract_id': res.id,
                'salary_rule_ids': salary_rule_vals,
                'ctc': res.wage
            })
            res.salary_structure_ids = record
        return res


class ContractSalaryStructure(models.Model):
    _name = "contract.salary.structure"
    _description = 'Contract Salary Structure'

    name = fields.Char(string='Contract Salary Structure', required=True)
    salary_rule_ids = fields.One2many('contract.salary.rule', 'salary_structure_id', 'Salary Structure Rule')
    salary_contract_id = fields.Many2one('hr.contract', 'Contract')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.INR'))
    ctc = fields.Monetary('CTC')


class ContractSalaryRule(models.Model):
    _name = "contract.salary.rule"
    _description = 'Contract Salary Rule'

    name = fields.Char(string='Contract Salary Rule', required=True)
    salary_structure_id = fields.Many2one('contract.salary.structure', 'Salary Structure')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.INR'))
    amount = fields.Monetary('Amount')
    employee_amount = fields.Monetary('Employee Amount')
    is_editable = fields.Boolean(string='Editable by Employee', default=True)
    is_basic = fields.Boolean(string='Is Basic')
    rule_type = fields.Selection([
        ('deduction', 'Deduction'),
        ('allowance', 'Allowance'),
        ('other', 'Other'),
    ], 'Rule Type', default='other', tracking=True, required=True)

