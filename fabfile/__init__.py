#coding:utf-8
from fabric.api import env

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

env.entity_dir = env.java_source_dir + '/example/project/entity'
env.entity_dao_dir = env.java_source_dir + '/example/project/entity/dao'
env.java_package_entity = 'example.project.entity'
env.java_package_entity_dao = 'example.project.entity.dao'
