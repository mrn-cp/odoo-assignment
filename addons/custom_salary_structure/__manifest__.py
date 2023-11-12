# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Custom Salary Structure",
    "version": "14.0.0.0.1",
    "category": "Payroll",
    "website": "https://github.com/mrn-cp/odoo-assignment/tree/main/addons/custom_salary_structure",
    "sequence": 38,
    "summary": "Manage your employee payroll salary structure and contract.",
    # "license": "LGPL-3",
    "author": "manas",
    "depends": [
        "payroll",
        "payroll_account",
        "hr_contract",
    ],
    "data": [
        "data/mail_template.xml",
        "views/hr_contract_views.xml",
        "views/custom_salary_template.xml",
        "views/success_template.xml",
    ],
    "demo": [],
    "application": True,
    'installable': True,
    'auto_install': False,

}
