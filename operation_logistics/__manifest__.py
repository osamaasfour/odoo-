# operation_logistics/__manifest__.py
{
    'name': "Logistics Operations",
    'summary': "Manage shipments, costs, and revenues for logistics companies.",
    'description': """
        This module allows users to create and manage shipments, track vendor costs,
        client invoices, and calculate the revenue for each shipment.
    """,
    'author': "Your Company Name", # اسم شركتك
    'website': "http://www.yourcompany.com", # موقع شركتك
    'category': 'Operations',
    'version': '1.0',
    'depends': [
        'base',
        'mail', # لإضافة إمكانيات التواصل (التعليقات، المتابعة)
        'sale', # للربط بوحدة المبيعات
        'account', # للربط بوحدة المحاسبة
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/shipment_views.xml',
        # يمكنك إضافة المزيد من ملفات الـ XML هنا لاحقًا (مثل القوائم، التقارير)
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3', # تأكد من استخدام رخصة Odoo Community المناسبة
}