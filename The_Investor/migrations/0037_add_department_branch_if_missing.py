from django.db import migrations


def forwards(apps, schema_editor):
    conn = schema_editor.connection
    cursor = conn.cursor()
    # Check if branch_id column exists in the Department table
    try:
        cursor.execute("PRAGMA table_info('The_Investor_department')")
        cols = [row[1] for row in cursor.fetchall()]
    except Exception:
        cols = []

    if 'branch_id' not in cols:
        # SQLite: add the integer column; do not attempt to add FK constraint here
        cursor.execute("ALTER TABLE The_Investor_department ADD COLUMN branch_id integer")


def reverse(apps, schema_editor):
    # No-op reverse: we don't remove the column automatically
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('The_Investor', '0036_alter_investor_branch_alter_investor_department'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
