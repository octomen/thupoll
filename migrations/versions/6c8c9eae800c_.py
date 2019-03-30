"""empty message

Revision ID: 6c8c9eae800c
Revises: 1f3623ade1e4
Create Date: 2019-03-29 22:42:58.124338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c8c9eae800c'
down_revision = '1f3623ade1e4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE volume RENAME TO vote')
    op.execute('ALTER INDEX volume_pkey RENAME TO vote_pkey')
    op.execute('ALTER INDEX volume_people_id_people_id_uidx RENAME TO vote_people_id_people_id_uidx')
    op.execute('ALTER TABLE vote RENAME CONSTRAINT "volume_people_id_fkey" TO "vote_people_id_fkey"')
    op.execute('ALTER TABLE vote RENAME CONSTRAINT "volume_themepoll_id_fkey" TO "vote_themepoll_id_fkey"')
    op.execute('ALTER SEQUENCE volume_id_seq RENAME TO vote_id_seq')


def downgrade():
    op.execute('ALTER SEQUENCE vote_id_seq RENAME TO volume_id_seq')
    op.execute('ALTER TABLE vote RENAME TO volume')
    op.execute('ALTER TABLE volume RENAME CONSTRAINT "vote_themepoll_id_fkey" TO "volume_themepoll_id_fkey"')
    op.execute('ALTER TABLE volume RENAME CONSTRAINT "vote_people_id_fkey" TO "volume_people_id_fkey"')
    op.execute('ALTER INDEX vote_people_id_people_id_uidx RENAME TO volume_people_id_people_id_uidx')
    op.execute('ALTER INDEX vote_pkey RENAME TO volume_pkey')
