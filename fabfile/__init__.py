#coding:utf-8
from fabric.api import env

import generate

env.project_name = "dropwitch-entity"

env.mysql_host = "localhost"
env.mysql_user = "root"
env.mysql_database = "example"

env.generated_dir = "generated"
env.schema_sql_dir = env.generated_dir + "/db/"
env.persistence_xml_dir = env.generated_dir + "/src/main/resources/META-INF"
env.entity_dir = env.generated_dir + "/src/main/java/com/github/dropwitch/entity"
env.entity_dao_base_dir = env.generated_dir + "/src/main/java/com/github/dropwitch/entity/dao/base"
env.java_package_entity = "com.github.dropwitch.entity"
env.java_package_entity_dao_base = "com.github.dropwitch.entity.dao.base"
