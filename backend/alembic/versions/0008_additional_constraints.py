"""Additional constraints

Revision ID: 0008
Revises: 0007
Create Date: 2025-04-01 04:44:32.146557

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op



# revision identifiers, used by Alembic.
revision: str = '0008'
down_revision: Union[str, None] = '0007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_columns_experiment_id_laboratory_experiments', 'columns', type_='foreignkey')
    op.create_foreign_key(op.f('fk_columns_experiment_id_laboratory_experiments'), 'columns', 'laboratory_experiments', ['experiment_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_computational_experiment_datas_input_id_schemas', 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint('fk_computational_experiment_datas_output_id_schemas', 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint('fk_computational_experiment_datas_context_id_schemas', 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint('fk_computational_experiment_datas_parameters_id_schemas', 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint('fk_computational_experiment_datas_experiment_id_computa_6406', 'computational_experiment_datas', type_='foreignkey')
    op.create_foreign_key(op.f('fk_computational_experiment_datas_context_id_schemas'), 'computational_experiment_datas', 'schemas', ['context_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key(op.f('fk_computational_experiment_datas_input_id_schemas'), 'computational_experiment_datas', 'schemas', ['input_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key(op.f('fk_computational_experiment_datas_parameters_id_schemas'), 'computational_experiment_datas', 'schemas', ['parameters_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key(op.f('fk_computational_experiment_datas_output_id_schemas'), 'computational_experiment_datas', 'schemas', ['output_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key(op.f('fk_computational_experiment_datas_experiment_id_computational_experiments'), 'computational_experiment_datas', 'computational_experiments', ['experiment_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_computational_experiment_templates_input_id_schemas', 'computational_experiment_templates', type_='foreignkey')
    op.drop_constraint('fk_computational_experiment_templates_parameters_id_schemas', 'computational_experiment_templates', type_='foreignkey')
    op.drop_constraint('fk_computational_experiment_templates_output_id_schemas', 'computational_experiment_templates', type_='foreignkey')
    op.drop_constraint('fk_computational_experiment_templates_context_id_schemas', 'computational_experiment_templates', type_='foreignkey')
    op.create_foreign_key(op.f('fk_computational_experiment_templates_input_id_schemas'), 'computational_experiment_templates', 'schemas', ['input_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key(op.f('fk_computational_experiment_templates_parameters_id_schemas'), 'computational_experiment_templates', 'schemas', ['parameters_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key(op.f('fk_computational_experiment_templates_output_id_schemas'), 'computational_experiment_templates', 'schemas', ['output_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key(op.f('fk_computational_experiment_templates_context_id_schemas'), 'computational_experiment_templates', 'schemas', ['context_id'], ['id'], ondelete='RESTRICT')
    op.drop_constraint('fk_computational_experiments_id_experiments', 'computational_experiments', type_='foreignkey')
    op.create_foreign_key(op.f('fk_computational_experiments_id_experiments'), 'computational_experiments', 'experiments', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_experiments_user_id_users', 'experiments', type_='foreignkey')
    op.create_foreign_key(op.f('fk_experiments_user_id_users'), 'experiments', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_laboratory_experiments_id_experiments', 'laboratory_experiments', type_='foreignkey')
    op.create_foreign_key(op.f('fk_laboratory_experiments_id_experiments'), 'laboratory_experiments', 'experiments', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_measurements_experiment_id_laboratory_experiments', 'measurements', type_='foreignkey')
    op.create_foreign_key(op.f('fk_measurements_experiment_id_laboratory_experiments'), 'measurements', 'laboratory_experiments', ['experiment_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_profiles_user_id_users', 'profiles', type_='foreignkey')
    op.create_foreign_key(op.f('fk_profiles_user_id_users'), 'profiles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_profiles_user_id_users'), 'profiles', type_='foreignkey')
    op.create_foreign_key('fk_profiles_user_id_users', 'profiles', 'users', ['user_id'], ['id'])
    op.drop_constraint(op.f('fk_measurements_experiment_id_laboratory_experiments'), 'measurements', type_='foreignkey')
    op.create_foreign_key('fk_measurements_experiment_id_laboratory_experiments', 'measurements', 'laboratory_experiments', ['experiment_id'], ['id'])
    op.drop_constraint(op.f('fk_laboratory_experiments_id_experiments'), 'laboratory_experiments', type_='foreignkey')
    op.create_foreign_key('fk_laboratory_experiments_id_experiments', 'laboratory_experiments', 'experiments', ['id'], ['id'])
    op.drop_constraint(op.f('fk_experiments_user_id_users'), 'experiments', type_='foreignkey')
    op.create_foreign_key('fk_experiments_user_id_users', 'experiments', 'users', ['user_id'], ['id'])
    op.drop_constraint(op.f('fk_computational_experiments_id_experiments'), 'computational_experiments', type_='foreignkey')
    op.create_foreign_key('fk_computational_experiments_id_experiments', 'computational_experiments', 'experiments', ['id'], ['id'])
    op.drop_constraint(op.f('fk_computational_experiment_templates_context_id_schemas'), 'computational_experiment_templates', type_='foreignkey')
    op.drop_constraint(op.f('fk_computational_experiment_templates_output_id_schemas'), 'computational_experiment_templates', type_='foreignkey')
    op.drop_constraint(op.f('fk_computational_experiment_templates_parameters_id_schemas'), 'computational_experiment_templates', type_='foreignkey')
    op.drop_constraint(op.f('fk_computational_experiment_templates_input_id_schemas'), 'computational_experiment_templates', type_='foreignkey')
    op.create_foreign_key('fk_computational_experiment_templates_context_id_schemas', 'computational_experiment_templates', 'schemas', ['context_id'], ['id'])
    op.create_foreign_key('fk_computational_experiment_templates_output_id_schemas', 'computational_experiment_templates', 'schemas', ['output_id'], ['id'])
    op.create_foreign_key('fk_computational_experiment_templates_parameters_id_schemas', 'computational_experiment_templates', 'schemas', ['parameters_id'], ['id'])
    op.create_foreign_key('fk_computational_experiment_templates_input_id_schemas', 'computational_experiment_templates', 'schemas', ['input_id'], ['id'])
    op.drop_constraint(op.f('fk_computational_experiment_datas_experiment_id_computational_experiments'), 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint(op.f('fk_computational_experiment_datas_output_id_schemas'), 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint(op.f('fk_computational_experiment_datas_parameters_id_schemas'), 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint(op.f('fk_computational_experiment_datas_input_id_schemas'), 'computational_experiment_datas', type_='foreignkey')
    op.drop_constraint(op.f('fk_computational_experiment_datas_context_id_schemas'), 'computational_experiment_datas', type_='foreignkey')
    op.create_foreign_key('fk_computational_experiment_datas_experiment_id_computa_6406', 'computational_experiment_datas', 'computational_experiments', ['experiment_id'], ['id'])
    op.create_foreign_key('fk_computational_experiment_datas_parameters_id_schemas', 'computational_experiment_datas', 'schemas', ['parameters_id'], ['id'])
    op.create_foreign_key('fk_computational_experiment_datas_context_id_schemas', 'computational_experiment_datas', 'schemas', ['context_id'], ['id'])
    op.create_foreign_key('fk_computational_experiment_datas_output_id_schemas', 'computational_experiment_datas', 'schemas', ['output_id'], ['id'])
    op.create_foreign_key('fk_computational_experiment_datas_input_id_schemas', 'computational_experiment_datas', 'schemas', ['input_id'], ['id'])
    op.drop_constraint(op.f('fk_columns_experiment_id_laboratory_experiments'), 'columns', type_='foreignkey')
    op.create_foreign_key('fk_columns_experiment_id_laboratory_experiments', 'columns', 'laboratory_experiments', ['experiment_id'], ['id'])
    # ### end Alembic commands ###
