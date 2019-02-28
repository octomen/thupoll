"""empty message

Revision ID: b4c2e2c75704
Revises: 5c345619908c
Create Date: 2019-02-28 23:48:40.967119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c2e2c75704'
down_revision = '5c345619908c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
        INSERT INTO role (id, name) VALUES
            (1, 'octopus'),
            (2, 'inhabitant');
    ''')

    op.execute('''
        INSERT INTO people (role_id, telegram_login) VALUES
            (2, '273204308'), -- Серёга
            (2, '278135592'), -- Саша
            (1, '339423039'); -- Даня
    ''')


def downgrade():
    op.execute('DELETE FROM people;')
    op.execute('DELETE FROM roles;')
