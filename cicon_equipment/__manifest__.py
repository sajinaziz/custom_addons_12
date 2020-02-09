{
    'name': 'CICON Equipment Extended',
    'version': '0.1',
    'author': 'CICON',
    'sequence': 99,
    'summary': 'CICON Equipment',
    'description': """CICON Equipment""",
    'website': 'http://www.cicon.net',
    'category': 'CICON IT',
    'depends': ['hr_maintenance', 'maintenance', 'purchase'],
    'data': [
        'security/cicon_equipment_security.xml',
        'security/ir.model.access.csv',
        'views/cicon_equipment_view.xml',
        'views/cicon_equipment_property_view.xml',
        'views/cicon_user_identity_view.xml',
        'views/cicon_equipment_seq.xml',
        'views/cicon_maintenance_request_view.xml',
        'views/cicon_equipment_ip_view.xml',
        'wizard/wizard_equip_ip_update_view.xml',
        'report/equipment_report.xml',
        'report/equipment_report_template.xml',
        'report/equipments_report_template_summary.xml',
        'report/maintenance_report.xml',
        'report/maintenance_report_template.xml',

    ],
    'update_xml': [],
    'description': 'CICON Applications',
    'active': False,
    'installable': True,
    'application': False,
    'auto_install': False
}
