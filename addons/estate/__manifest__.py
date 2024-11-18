{
    'name': 'Estate Management',
    'version': '1.0',
    'summary': 'Module for managing real estate properties',
    'sequence': 10,
    'description': """
Estate Management Module
=======================
Module to manage real estate properties, buyers, and sellers.
    """,
    'category': 'Real Estate',
    'author': 'Hoang Hai Nam',
    'depends': ['base'],
    'data': ['security/ir.model.access.csv',
             'data/estate_property_type_data.xml',
             'data/estate_property_tag_data.xml',
             'views/actions.xml',
             'views/estate_menus.xml',
             'views/estate_property_views.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_tag_views.xml',
             'views/estate_property_offer_views.xml',
             'views/res_users_views.xml',],
    'installable': True,
    'application': True,
    'auto_install': False,
}
