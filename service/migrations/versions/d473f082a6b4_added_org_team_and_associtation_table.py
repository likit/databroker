"""added org team and associtation table

Revision ID: d473f082a6b4
Revises: c43f2f13bb95
Create Date: 2019-10-04 10:14:42.848684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd473f082a6b4'
down_revision = 'c43f2f13bb95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('org_team',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('org_client_team',
    sa.Column('org_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['org_id'], ['org_client.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['org_team.id'], ),
    sa.PrimaryKeyConstraint('org_id', 'team_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('org_client_team')
    op.drop_table('org_team')
    # ### end Alembic commands ###
