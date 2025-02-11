{
    "name": "Attendance-Customization",
    "author": "Muhammad Usman Hussain",
    "License": "LGPL-3",
    "version": "1.0",
    'category': 'Human Resources',
    'summary': 'Track Employee Attendance with Arrival and Departure Times',
    'description': """
            This module offers the basic functionalities to manage attendance.
    """,
    "depends": ["base", "hr_contract", "hr",

                ],
    "data": [
        "views/attendance_view.xml",
        "views/template.xml",
    ],
    'installable': True,
    'application': True,
}
