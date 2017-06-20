#coding:utf-8
from fabric.api import env

import os
import generate

# Please edit following strings (inside '')

env.generated_dir = 'generated'
env.project_name = 'example-entity'

env.mysql = [
    {'host': 'localhost', 'user': 'your_mysql_user_name', 'database': 'your_database_name'},
]

_project_dir = 'example/project'
_project_package = 'example.project'

# Please edit above strings (inside '')

env.schema_sql_dir = env.generated_dir + '/db'
env.source_dir = env.generated_dir + '/src'
env.persistence_xml_dir = env.source_dir + '/main/resources/META-INF'
env.java_source_dir = env.source_dir + '/main/java'

env.entity_dir = os.path.join(env.java_source_dir, _project_dir, 'entity')
env.entity_dao_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/dao')
env.entity_dao_impl_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/dao/impl')
env.entity_ext_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/ext')
env.entity_dao_ext_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/dao/ext')
env.entity_dao_ext_impl_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/dao/ext/impl')

env.java_package_entity = _project_package + '.entity'
env.java_package_entity_dao = _project_package + '.entity.dao'
env.java_package_entity_dao_impl = _project_package + '.entity.dao.impl'
env.java_package_entity_ext = _project_package + '.entity.ext'
env.java_package_entity_dao_ext = _project_package + '.entity.dao.ext'
env.java_package_entity_dao_ext_impl = _project_package + '.entity.dao.ext.impl'
