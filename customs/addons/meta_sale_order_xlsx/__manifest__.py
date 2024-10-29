# -*- coding: utf-8 -*-
{
    'name': "Sale Order Excel Report",

    'summary': """
        """,

    'description': """

    """,

    'maintainer': 'Metamorphosis',
    'author': "Metamorphosis",
    'co-author': "Rifat Anwar",
    'website': "https://metamorphosis.com.bd",
    'category': 'Tools/Tools',
    'version': '18.0.1.0',
    'depends': ['sale', 'report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'report/sale_order_report_xlsx.xml',
        'wizard/wizard_xlsx.xml',
        'wizard/sale_order_wizard_report_xlsx.xml'
    ],
    "license": "LGPL-3",
    "sequence": -10,
    "application": True,
    "installable": True,
    "auto_install": False,
}
