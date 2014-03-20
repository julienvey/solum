#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""add default data to service

Revision ID: e9e025e1f28
Revises: 12d90235e174
Create Date: 2014-03-20 14:05:00.527818

"""
import uuid

from alembic import op
import sqlalchemy as sa

from solum.openstack.common import timeutils

# revision identifiers, used by Alembic.
revision = 'e9e025e1f28'
down_revision = '12d90235e174'


def upgrade():
    service_table = sa.sql.table('service',
                                 sa.sql.column('uuid', sa.Integer),
                                 sa.sql.column('name', sa.String(36)),
                                 sa.sql.column('created_at', sa.DateTime),
                                 sa.sql.column('description', sa.String(36)),
                                 sa.sql.column('read_only', sa.Boolean),
                                 sa.sql.column('service_type', sa.String(100)))
    op.execute(service_table.insert().values(
        {"uuid": uuid.uuid4(),
         "name": "language_pack service",
         "created_at": timeutils.utcnow(),
         "description": "generic service for all language_pack objects",
         "service_type": "language_pack",
         "read_only": False
         }))


def downgrade():
    service_table = sa.sql.table('service',
                                 sa.sql.column('service_type', sa.String(100)))
    op.execute(service_table.delete().where(
        service_table.c.service_type == op.inline_literal("language_pack")))
