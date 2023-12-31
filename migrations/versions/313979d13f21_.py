"""empty message

Revision ID: 313979d13f21
Revises: 
Create Date: 2023-07-12 06:58:38.346709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '313979d13f21'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_name', sa.String(length=255), nullable=False),
    sa.Column('admin_password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('category',
    sa.Column('cat_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cat_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('cat_id')
    )
    op.create_table('contact',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cont_name', sa.String(length=255), nullable=False),
    sa.Column('cont_phone', sa.String(length=20), nullable=False),
    sa.Column('cont_email', sa.String(length=255), nullable=False),
    sa.Column('cont_msg', sa.Text(), nullable=False),
    sa.Column('cont_reg_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_fname', sa.String(length=255), nullable=False),
    sa.Column('user_email', sa.String(length=255), nullable=False),
    sa.Column('user_password', sa.String(length=20), nullable=False),
    sa.Column('user_country', sa.String(length=50), nullable=False),
    sa.Column('user_desc', sa.String(length=120), nullable=True),
    sa.Column('user_lang', sa.String(length=120), nullable=True),
    sa.Column('user_lang_level', sa.String(length=120), nullable=True),
    sa.Column('user_skill', sa.String(length=120), nullable=True),
    sa.Column('user_skill_level', sa.String(length=120), nullable=True),
    sa.Column('user_pix', sa.String(length=120), nullable=True),
    sa.Column('user_reg_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('portfolio',
    sa.Column('Portfolio_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('sample1', sa.String(length=255), nullable=False),
    sa.Column('port_userid', sa.Integer(), nullable=False),
    sa.Column('port_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['port_userid'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('Portfolio_id')
    )
    op.create_table('rating',
    sa.Column('rating_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rat_userid', sa.Integer(), nullable=False),
    sa.Column('rat_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['rat_userid'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('rating_id')
    )
    op.create_table('subcategory',
    sa.Column('subcat_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subcat_name', sa.String(length=255), nullable=False),
    sa.Column('subcat_catid', sa.Integer(), nullable=False),
    sa.Column('subcat_titile', sa.Text(), nullable=False),
    sa.Column('subcat_cover', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subcat_catid'], ['category.cat_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('subcat_id')
    )
    op.create_table('project',
    sa.Column('Project_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_name', sa.String(length=255), nullable=False),
    sa.Column('details', sa.String(length=255), nullable=False),
    sa.Column('budject', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('project_catid', sa.Integer(), nullable=False),
    sa.Column('project_subcatid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_catid'], ['category.cat_id'], ),
    sa.ForeignKeyConstraint(['project_subcatid'], ['subcategory.subcat_id'], ),
    sa.PrimaryKeyConstraint('Project_id')
    )
    op.create_table('projectbid',
    sa.Column('projectbid_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.Column('probid_projectid', sa.Integer(), nullable=False),
    sa.Column('probid_freelancerid', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['probid_freelancerid'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['probid_projectid'], ['project.Project_id'], ),
    sa.PrimaryKeyConstraint('projectbid_id')
    )
    op.create_table('payment',
    sa.Column('Pay_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('pay_userid', sa.Integer(), nullable=False),
    sa.Column('pay_bidid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pay_bidid'], ['projectbid.projectbid_id'], ),
    sa.ForeignKeyConstraint(['pay_userid'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('Pay_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    op.drop_table('projectbid')
    op.drop_table('project')
    op.drop_table('subcategory')
    op.drop_table('rating')
    op.drop_table('portfolio')
    op.drop_table('user')
    op.drop_table('contact')
    op.drop_table('category')
    op.drop_table('admin')
    # ### end Alembic commands ###
