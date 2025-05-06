{
    'name': 'IP Restricted Attendance with Todo',
    'version': '18.0.1.0.5',
    'summary': 'Employee attendance system with IP restriction and task management',
    'description': """
        Comprehensive employee attendance system with:
        - IP address restriction for check-in/out
        - Break time tracking
        - Todo task integration
        - Employee dashboard
    """,
    'category': 'Human Resources',
    'author': 'Your Name',
    'company': 'Your Company',
    'website': 'https://yourwebsite.com',
    'depends': [
        'base',
        'hr',
        'hr_attendance',
        'crm',  # For Todo tasks
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/attendance_views.xml',
        'views/todo_views.xml',
        'views/templates.xml',
        'views/menu_views.xml',
        'views/break_views.xml',
    ],
    'migrations': ['migrations/18.0.1.0.5/pre-migrate.py'],
    'assets': {
        'web.assets_backend': [
            'ip_restricted_attendance/static/src/css/attendance.css',
            'ip_restricted_attendance/static/src/js/attendance_dashboard.js',
        ],
    },
    'demo': [],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}