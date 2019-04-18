"""init db

Revision ID: 3e75201aa606
Revises: 
Create Date: 2019-03-24 17:47:16.351704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e75201aa606'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('_password_hash', sa.String(length=255), nullable=True),
    sa.Column('blog_title', sa.String(length=60), nullable=True),
    sa.Column('blog_sub_title', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('about', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_admin'))
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_category')),
    sa.UniqueConstraint('name', name=op.f('uq_category_name'))
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name=op.f('fk_post_category_id_category')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post'))
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=254), nullable=True),
    sa.Column('site', sa.String(length=255), nullable=True),
    sa.Column('body', sa.String(length=200), nullable=True),
    sa.Column('from_admin', sa.Boolean(), nullable=True),
    sa.Column('reviewed', sa.Boolean(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('replied_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_comment_post_id_post')),
    sa.ForeignKeyConstraint(['replied_id'], ['comment.id'], name=op.f('fk_comment_replied_id_comment')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comment'))
    )
    op.create_index(op.f('ix_comment_author'), 'comment', ['author'], unique=False)
    op.create_index(op.f('ix_comment_timestamp'), 'comment', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_timestamp'), table_name='comment')
    op.drop_index(op.f('ix_comment_author'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('category')
    op.drop_table('admin')
    # ### end Alembic commands ###
