{
    'name': 'Custom Excel Report',
    'category': 'sale',
    'version': '0.0.0.1',
    'summary': 'This module provides generated excel report',
    'website': ' ',
    'author': 'Crystal Technology Bangladesh Ltd.',
    'license': 'AGPL-3',
    'description': '''This module provides generated excel report.
                      '''
                   ,
    'depends': ['base','sale','stock','stock_account','account','report_xlsx'],
    'data': [
        'views/inherited_view.xml',
        'views/inherited_view_balance_sheet.xml',
        'views/custom_xlsx.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
