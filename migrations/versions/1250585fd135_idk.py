"""idk

Revision ID: 1250585fd135
Revises: d711cc8805f1
Create Date: 2024-01-25 20:23:50.944162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1250585fd135'
down_revision = 'd711cc8805f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['book_id'])

    with op.batch_alter_table('users_books', schema=None) as batch_op:
        batch_op.alter_column('doi',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'books', ['book_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_books', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'books', ['book_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('doi',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)

    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
