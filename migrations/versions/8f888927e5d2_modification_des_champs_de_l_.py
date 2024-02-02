"""modification des champs de l'utilisateurs enlèvement du champ prenom  migration.

Revision ID: 8f888927e5d2
Revises: fbb9641cad95
Create Date: 2024-01-27 22:33:08.461187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f888927e5d2'
down_revision = 'fbb9641cad95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.drop_column('prenom')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prenom', sa.VARCHAR(length=250), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
