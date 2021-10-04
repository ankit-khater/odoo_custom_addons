{

    'name': 'Doctor_Referral',
    'version': '1.0.0.2',
    'summary': 'Custom Doctor Referral requirement for SF',
    'sequence': 1,
    'category': 'Tools',
    'website': '',
    'images': [],
    'depends': ['sale', 'sale_stock','sales_team','point_of_sale','account'],
    'data': ['views/doctor_view.xml',
             'views/res_doctor_menu.xml',
             'views/doctor_department_view.xml',
             'views/doctor_department_menu.xml',
             'views/sale_order_custom_view.xml','views/account_invoice_custom.xml',
             'views/res_consultant_menu.xml',
             'views/consultant_view.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}