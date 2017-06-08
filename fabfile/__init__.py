#coding:utf-8
from fabric.api import env

import os
import generate

env.generated_dir = 'generated'
env.schema_sql_dir = env.generated_dir + '/db'
env.source_dir = env.generated_dir + '/src'
env.persistence_xml_dir = env.source_dir + '/main/resources/META-INF'
env.java_source_dir = env.source_dir + '/main/java'

# Please edit following strings (inside '')

env.project_name = 'example-entity'

env.mysql_host = 'localhost'
env.mysql_user = 'your_mysql_user_name'
env.mysql_database = 'your_database_name'

_project_dir = 'example/project'
_project_package = 'example.project'

# Please edit above strings (inside '')

env.entity_dir = os.path.join(env.java_source_dir, _project_dir, 'entity')
env.entity_dao_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/dao')
env.entity_ext_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/ext')
env.entity_dao_ext_dir = os.path.join(env.java_source_dir, _project_dir, 'entity/dao/ext')

env.java_package_entity = _project_package + '.entity'
env.java_package_entity_dao = _project_package + '.entity.dao'
env.java_package_entity_ext = _project_package + '.entity.ext'
env.java_package_entity_dao_ext = _project_package + '.entity.dao.ext'
