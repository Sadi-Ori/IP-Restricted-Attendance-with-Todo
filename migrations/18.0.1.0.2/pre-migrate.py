from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Let Odoo handle the schema changes through ORM
    env['ir.model'].search([('model', '=', 'hr.employee')])._prepare_model()

    # Check if table exists first
    cr.execute("""
        SELECT 1 FROM pg_tables 
        WHERE tablename = 'ip_restricted_attendance_attendance_device'
    """)
    if cr.fetchone():
        cr.execute("""
            ALTER TABLE hr_attendance
            ADD COLUMN IF NOT EXISTS device_id integer,
            ADD COLUMN IF NOT EXISTS check_out_device_id integer
        """)

        cr.execute("""
            ALTER TABLE hr_attendance
            ADD CONSTRAINT hr_attendance_device_id_fkey 
            FOREIGN KEY (device_id) 
            REFERENCES ip_restricted_attendance_attendance_device(id)
        """)

        cr.execute("""
            ALTER TABLE hr_attendance
            ADD CONSTRAINT hr_attendance_check_out_device_id_fkey 
            FOREIGN KEY (check_out_device_id) 
            REFERENCES ip_restricted_attendance_attendance_device(id)
        """)