"""empty message

Revision ID: 0d5a315661ae
Revises: 
Create Date: 2017-08-13 19:03:13.608649

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '0d5a315661ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    grants_table = op.create_table('grants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date_time', sa.DateTime(), nullable=True),
    sa.Column('update_date_time', sa.DateTime(), nullable=True),
    sa.Column('delete_date_time', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    tokens_table = op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date_time', sa.DateTime(), nullable=True),
    sa.Column('update_date_time', sa.DateTime(), nullable=True),
    sa.Column('delete_date_time', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date_time', sa.DateTime(), nullable=True),
    sa.Column('update_date_time', sa.DateTime(), nullable=True),
    sa.Column('delete_date_time', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=300), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('password_hash', sa.String(length=4000), nullable=True),
    sa.Column('is_verified_email', sa.Boolean(), nullable=True),
    sa.Column('is_locked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('children',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date_time', sa.DateTime(), nullable=True),
    sa.Column('update_date_time', sa.DateTime(), nullable=True),
    sa.Column('delete_date_time', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=300), nullable=False),
    sa.Column('middle_name', sa.String(length=300), nullable=True),
    sa.Column('last_name', sa.String(length=300), nullable=False),
    sa.Column('date_of_birth', sa.DateTime(), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_grants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date_time', sa.DateTime(), nullable=True),
    sa.Column('update_date_time', sa.DateTime(), nullable=True),
    sa.Column('delete_date_time', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('grant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grant_id'], ['grants.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date_time', sa.DateTime(), nullable=True),
    sa.Column('update_date_time', sa.DateTime(), nullable=True),
    sa.Column('delete_date_time', sa.DateTime(), nullable=True),
    sa.Column('token_hash', sa.String(length=4000), nullable=False),
    sa.Column('expires_date_time', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['token_id'], ['tokens.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token_hash')
    )
    op.create_table('user_children',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date_time', sa.DateTime(), nullable=True),
    sa.Column('update_date_time', sa.DateTime(), nullable=True),
    sa.Column('delete_date_time', sa.DateTime(), nullable=True),
    sa.Column('is_primary', sa.Boolean(), nullable=False),
    sa.Column('child_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['children.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    op.bulk_insert(grants_table,
                   [
                       {'id': 1, 'name': 'facebook', 'is_enabled': True, 'create_date_time': datetime.utcnow()}
                   ])
    op.bulk_insert(tokens_table,
                   [
                       {'id': 1, 'name': 'ResetPassword', 'create_date_time': datetime.utcnow()},
                       {'id': 2, 'name': 'VerifyEmail', 'create_date_time': datetime.utcnow()}
                   ])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_children')
    op.drop_table('user_tokens')
    op.drop_table('user_grants')
    op.drop_table('children')
    op.drop_table('users')
    op.drop_table('tokens')
    op.drop_table('grants')
    # ### end Alembic commands ###
