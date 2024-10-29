# -*- coding: utf-8 -*-
{
    'name': "Sale Order Pivot Inherit",

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
    'depends': ['sale'],

    'data': [
        'views/sale_order_inherit_template.xml',
        'views/sale_report_inherit_pivot.xml',
    ],
    "license": "LGPL-3",
    "sequence": -10,
    "application": True,
    "installable": True,
    "auto_install": False,
}
