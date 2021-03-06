# coding:utf-8
from fabric.api import env, local, lcd
from fabric.colors import green
from fabric.decorators import task
from jinja2 import Environment, FileSystemLoader

import os
import re

from Class import *

FAB_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.normpath(FAB_DIR + '/../')
SCHEMA_SQL_DIR = ''
SCHEMA_SQL_PATH = ''


@task
def clean():
    with lcd(PROJECT_DIR):
        # Clean java
        _java_clean()

        # Clean python fabric
        _set_schema_dir()
        local('rm -f ' + env.schema_sql_dir + '/schema.sql')
        local('rm -f ' + env.generated_dir + '/*.gradle')
        local('rm -f ' + env.persistence_xml_dir + '/*.xml')
        local('rm -f ' + env.entity_dir + '/Abstract*.java')
        local('rm -f ' + env.entity_dao_dir + '/Abstract*Dao.java')
        local('rm -f ' + env.entity_dao_impl_dir + '/Abstract*DaoImpl.java')


@task
def schema():
    with lcd(PROJECT_DIR):
        _set_schema_dir()

        # Create output dir if not exists
        local("[ -d {0} ] || mkdir -p {0}".format(SCHEMA_SQL_DIR))

        # Initialize output file
        local('echo "" > ' + SCHEMA_SQL_PATH)

        for mysql in env.mysql:
            _output_schema(mysql)

        # Reset auto increment counter
        sed_inplace(SCHEMA_SQL_PATH, 'AUTO_INCREMENT=\d* ', '')

        print green('schema.sql has been generated!')


@task
def code(version, no_xml = False):
    with lcd(PROJECT_DIR):
        env.build_version = version
        _generate_entities(no_xml)
        print green('Java files have been generated!')


@task
def jar():
    with lcd(PROJECT_DIR):
        _java_build()
        print green('JAR file has been generated:')
        jar_path = os.path.join(env.generated_dir, "build/libs/{0}-*.jar".format(env.project_name))
        local('ls ' + jar_path)


def _generate_entities(no_xml):
    _set_schema_dir()
    databases = _parse_sql()
    _print_tables(databases)
    _tables_to_files(databases, no_xml)


def _set_schema_dir():
    global SCHEMA_SQL_DIR
    global SCHEMA_SQL_PATH
    SCHEMA_SQL_DIR = os.path.join(PROJECT_DIR, env.schema_sql_dir)
    SCHEMA_SQL_PATH = os.path.join(SCHEMA_SQL_DIR, 'schema.sql')


def _output_schema(mysql):
    # Options
    ignore_tables = ''
    for database in mysql['databases']:
        ignore_tables += " --ignore-table {0}.DATABASECHANGELOG --ignore-table {0}.DATABASECHANGELOGLOCK --ignore-table {0}.schema_version".format(database)
    opts = '--no-data --compact --quick --single-transaction' + ignore_tables
    databases = ' '.join(mysql['databases'])

    # Execute mysqldump
    print(mysql.has_key('password'))
    if mysql.has_key('password'):
        password = ' -p' + mysql['password'] if mysql['password'] else ''
        local('mysqldump ' + opts + ' -h' + mysql['host'] + ' -u' + mysql['user'] + password + ' -B ' + databases + ' >> ' + SCHEMA_SQL_PATH)
    else:
        local('mysqldump ' + opts + ' -h' + mysql['host'] + ' -u' + mysql['user'] + ' -p -B ' + databases + ' >> ' + SCHEMA_SQL_PATH)


def _parse_sql():
    # Compiled regex patterns
    use_database = re.compile('^USE `(.*?)`;', re.IGNORECASE)
    create_table = re.compile('^CREATE TABLE `(.*?)`', re.IGNORECASE)
    column = re.compile('^\s*?`(?P<name>.*?)` (?P<type>\w.*?)[,\s]((?P<unsigned>unsigned)[,\s])?(.*?(?P<not_null>NOT\sNULL).*?[,\s])?(DEFAULT \'(?P<default>.*)\'[,\s])?((?P<auto_increment>AUTO_INCREMENT)[,\s])?', re.IGNORECASE)
    primary_key = re.compile('^\s*?(?P<type>PRIMARY KEY) .*?\((?P<columns>(`\w.*?`,?)+.*?)\)[,]?$', re.IGNORECASE)
    unique_key = re.compile('^\s*?(?P<type>UNIQUE KEY) .*?\((?P<columns>(`\w.*?`,?)+.*?)\)[,]?$', re.IGNORECASE)
    key = re.compile('^\s*?(?P<type>KEY) .*?\((?P<columns>(`\w.*?`,?)+.*?)\)[,]?$', re.IGNORECASE)
    column_of_key = re.compile('`(\w.*?)`', re.IGNORECASE)
    create_table_end = re.compile('^\)')

    databases = []
    with open(SCHEMA_SQL_PATH) as f:
        database = None
        persistence_unit_name = ''

        for line in f:
            # parse database name
            matches = use_database.match(line)
            if matches:
                database_name = matches.group(1)
                persistence_unit_name = env.persistence_unit_name_map[database_name]
                database = Database(database_name, persistence_unit_name)
                databases.append(database)
                continue

            # parse table name
            matches = create_table.match(line)
            if matches:
                table_name = matches.group(1)
                database.get_tables().append(Table(table_name, persistence_unit_name))
                continue

            # parse column name
            matches = column.match(line)
            if matches:
                table = database.get_tables().pop()
                table.add_column(Column(matches.group('name'), matches.group('type'), matches.group('unsigned'), matches.group('not_null'), matches.group('default'), matches.group('auto_increment')))
                database.get_tables().append(table)

            # parse primary key
            matches = primary_key.match(line)
            if matches:
                table = database.get_tables().pop()
                i = Index(matches.group('type'))
                column_names = column_of_key.findall(matches.group('columns'))
                i.set_column_names(column_names)
                # find and add Column object
                for name in column_names:
                    i.add_column(table.find_column_by_name(name))
                table.add_index(i)
                database.get_tables().append(table)

            # parse unique keys
            matches = unique_key.match(line)
            if matches:
                table = database.get_tables().pop()
                i = Index(matches.group('type'))
                column_names = column_of_key.findall(matches.group('columns'))
                i.set_column_names(column_names)
                # find and add Column object
                for name in column_names:
                    i.add_column(table.find_column_by_name(name))
                table.add_index(i)
                database.get_tables().append(table)

            # parse keys
            matches = key.match(line)
            if matches:
                table = database.get_tables().pop()
                i = Index(matches.group('type'))
                column_names = column_of_key.findall(matches.group('columns'))
                i.set_column_names(column_names)
                # find and add Column object
                for name in column_names:
                    i.add_column(table.find_column_by_name(name))
                table.add_index(i)
                database.get_tables().append(table)

            matches = create_table_end.match(line)
            if matches:
                continue

    return databases


def _print_tables(databases):
    for database in databases:
        for table in database.get_tables():
            print '+', database.get_name() + '.' + table.get_name()
            print '  + columns'
            for column in table.get_columns():
                print '    -',
                print column.get_name(),
                print column.get_type() + ' ' + column.get_unsigned(),
                print 'NOT NULL' if column.is_not_null() else 'NULL',
                print column.get_default(),
                print column.get_auto_increment()

            print '  + indices'
            for index in table.get_indices():
                print '    *',
                print index.get_type(),
                print index.get_column_names()


def _tables_to_files(databases, no_xml):
    jinja_env = Environment(loader=FileSystemLoader(os.path.join(FAB_DIR, 'templates')), trim_blocks=True, lstrip_blocks=True)
    settings_gradle = jinja_env.get_template('settings.gradle.j2')
    build_gradle = jinja_env.get_template('build.gradle.j2')
    persistence_xml = jinja_env.get_template('persistence.xml.j2')
    abstract_entity = jinja_env.get_template('abstract_entity.j2')
    entity = jinja_env.get_template('entity.j2')
    abstract_dao = jinja_env.get_template('abstract_dao.j2')
    abstract_dao_impl = jinja_env.get_template('abstract_dao_impl.j2')
    abstract_entity_dao = jinja_env.get_template('abstract_entity_dao.j2')
    abstract_entity_dao_impl = jinja_env.get_template('abstract_entity_dao_impl.j2')
    entity_dao = jinja_env.get_template('entity_dao.j2')
    entity_dao_impl = jinja_env.get_template('entity_dao_impl.j2')

    # Create output dir if not exists
    local("[ -d {0} ] || mkdir -p {0}".format(env.generated_dir))

    # Generate settings.gradle
    settings_gradle_path = os.path.join(PROJECT_DIR, env.generated_dir, 'settings.gradle')
    settings_gradle.stream(
        env=env
    ).dump(settings_gradle_path)

    # Generate build.gradle
    build_gradle_path = os.path.join(PROJECT_DIR, env.generated_dir, 'build.gradle')
    build_gradle.stream(
        env=env
    ).dump(build_gradle_path)

    if not no_xml:
        # Generate persistence.xml
        local("[ -d {0} ] || mkdir -p {0}".format(env.persistence_xml_dir))
        persistence_xml_path = os.path.join(PROJECT_DIR, env.persistence_xml_dir, 'persistence.xml')
        persistence_xml.stream(
            env=env,
            databases=databases
        ).dump(persistence_xml_path)

    # Generate AbstractEntity.java
    local("[ -d {0} ] || mkdir -p {0}".format(env.entity_dir))
    for database in databases:
        for table in database.get_tables():
            abstract_entity_path = os.path.join(PROJECT_DIR, env.entity_dir, 'Abstract' + table.get_class_name() + '.java')
            abstract_entity.stream(
                env=env,
                table=table
            ).dump(abstract_entity_path)

    # Generate Entity.java
    for database in databases:
        dir = os.path.join(env.entity_ext_dir, database.package_name)
        local("[ -d {0} ] || mkdir -p {0}".format(dir))
        for table in database.get_tables():
            entity_ext_path = os.path.join(PROJECT_DIR, dir, table.get_class_name() + '.java')
            # Prevent overwriting extension class
            if not os.path.isfile(entity_ext_path):
                entity.stream(
                    env=env,
                    table=table
                ).dump(entity_ext_path)

    # Generate AbstractDao.java
    local("[ -d {0} ] || mkdir -p {0}".format(env.entity_dao_dir))
    abstract_dao_path = os.path.join(PROJECT_DIR, env.entity_dao_dir, 'AbstractDao.java')
    abstract_dao.stream(
        env=env
    ).dump(abstract_dao_path)

    # Generate AbstractDaoImpl.java
    local("[ -d {0} ] || mkdir -p {0}".format(env.entity_dao_impl_dir))
    abstract_dao_impl_path = os.path.join(PROJECT_DIR, env.entity_dao_impl_dir, 'AbstractDaoImpl.java')
    abstract_dao_impl.stream(
        env=env
    ).dump(abstract_dao_impl_path)

    # Generate AbstractEntityDao.java
    for database in databases:
        for table in database.get_tables():
            abstract_entity_dao_path = os.path.join(PROJECT_DIR, env.entity_dao_dir, 'Abstract' + table.get_class_name() + 'Dao.java')
            abstract_entity_dao.stream(
                env=env,
                table=table,
            ).dump(abstract_entity_dao_path)

    # Generate AbstractEntityDaoImpl.java
    for database in databases:
        for table in database.get_tables():
            abstract_entity_dao_impl_path = os.path.join(PROJECT_DIR, env.entity_dao_impl_dir, 'Abstract' + table.get_class_name() + 'DaoImpl.java')
            abstract_entity_dao_impl.stream(
                env=env,
                table=table,
                database=database
            ).dump(abstract_entity_dao_impl_path)

    # Generate EntityDao.java
    local("[ -d {0} ] || mkdir -p {0}".format(env.entity_dao_ext_dir))
    for database in databases:
        for table in database.get_tables():
            entity_dao_path = os.path.join(PROJECT_DIR, env.entity_dao_ext_dir, table.get_class_name() + 'Dao.java')
            # Prevent overwriting extension class
            if not os.path.isfile(entity_dao_path):
                entity_dao.stream(
                    env=env,
                    table=table
                ).dump(entity_dao_path)

    # Generate EntityDaoImpl.java
    local("[ -d {0} ] || mkdir -p {0}".format(env.entity_dao_ext_impl_dir))
    for database in databases:
        for table in database.get_tables():
            entity_dao_impl_path = os.path.join(PROJECT_DIR, env.entity_dao_ext_impl_dir, table.get_class_name() + 'DaoImpl.java')
            # Prevent overwriting extension class
            if not os.path.isfile(entity_dao_impl_path):
                entity_dao_impl.stream(
                    env=env,
                    table=table
                ).dump(entity_dao_impl_path)


def _java_build():
    build_dir = os.path.join(PROJECT_DIR, env.generated_dir)
    with lcd(build_dir):
        local('./gradlew clean build')


def _java_clean():
    build_dir = os.path.join(PROJECT_DIR, env.generated_dir)
    with lcd(build_dir):
        if os.path.isfile('./gradlew'):
            local('./gradlew clean')
