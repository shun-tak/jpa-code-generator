# JPA code generator

Java Persistence code generator, working with supplied MySQL database.

JPA code generator generates following:
- a JPA configuration file (persistence.xml)
- JPA annotated model classes (Entity)
- JPA Static Metamodel classes (_Entity)
- Basic DAO classes (EntityDao)
- a JAR file which contains config and classes above

There are 2 commands following:
- `fab generate.schema`
  - reverse engineering existing MySQL tables into a schema file (schema.sql)
  - requires MySQL connection with `mysqldump` command
- `fab generate.jar`
  - generate a JAR file from schema.sql

Generated codes are dependent on Hibernate ORM implementation for now.


## Dependencies

Dependencies for this generator, not for generated sources.

- MySQL client 5.6 (`mysqldump` command)
- Python 2.7
- fabric
- jinja2 (Python template module)


## Usage

Fork or clone this repo.

Edit `env` in fabfile/\__init\__.py:

```
env.project_name = 'example-entity'

env.mysql_host = 'localhost'
env.mysql_user = 'your_mysql_user_name'
env.mysql_database = 'your_database_name'

_project_dir = 'example/project'
_project_package = 'example.project'
```

Run schema file generator:

```
fab generate.schema
```

Run jar file generator with your build version:

```
fab generate.jar:<version>
```

e.g. `fab generate.jar:1.0.0-SNAPSHOT`
