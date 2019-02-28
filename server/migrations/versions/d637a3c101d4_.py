"""
empty message

Revision ID: 2d8179b3a824
Revises: 98f53ae55150
Create Date: 2019-02-28 23:09:24.065895
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '2d8179b3a824'
down_revision = 'b74f90141cb1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
        INSERT INTO people (telegram_login) VALUES
            ('273204308'), -- Серёга
            ('278135592'), -- Саша
            ('339423039'); -- Даня
    ''')


def downgrade():
    op.execute('''
        DELETE FROM people WHERE telegram_login IN
            ('273204308', '278135592', '339423039');
    ''')
