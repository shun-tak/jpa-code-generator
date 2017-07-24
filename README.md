# JPA code generator

Java Persistence code generator, working with supplied MySQL database.

JPA code generator generates following:
- a JPA configuration file (persistence.xml)
- JPA annotated model classes (Entity)
- JPA Static Metamodel classes (_Entity)
- Basic DAO classes (EntityDao)
- a JAR file which contains config and classes above

[Example generated codes](https://github.com/shun-tak/jpa-code-generator-example)

You can see available commands with `fab -l`:
- `fab generate.schema`
  - reverse engineering existing MySQL tables into a schema file (schema.sql)
  - requires MySQL connection with `mysqldump` command
- `fab generate.code:<version>`
  - generate java codes from schema.sql
- `fab generate.jar`
  - generate a JAR file from generated java codes
- `fab generate.clean`
  - remove schema.sql and java codes excluding gap codes (extension classes)

Generated codes are dependent on Hibernate ORM implementation for now.


## Dependencies

Dependencies for this generator, not for generated sources.

- MySQL client 5.6 (`mysqldump` command)
- Python 2.7
- fabric
- jinja2 (Python template module)


## Usage

Fork or clone this repo.

### Configuration

Edit `env` in fabfile/\__init\__.py:

```
env.generated_dir = 'generated'
env.project_name = 'example-entity'

env.mysql = [
    # Input password interactively
    {'host': 'localhost', 'user': 'your_mysql_user_name', 'databases': ['your_database_name']},
    # Input password on batch
    {'host': 'localhost', 'user': 'your_mysql_user_name', 'password': 'your_mysql_password', 'databases': ['your_database_name']},
]

env.persistence_unit_name_map = {
    'your_database_name': 'your_persistence_unit_name'
}

_project_dir = 'example/project'
_project_package = 'example.project'
```

### Schema file generator

```
fab generate.schema
```

### Java files generator

Run with your build version:

```
fab generate.code:<version>
```

e.g. `fab generate.code:1.0.0-SNAPSHOT`

If you don't need persistence.xml, you can add `no_xml` option:

```
fab generate.code:<version>,no_xml=True
```

then you can skip generating persistence.xml.

### Jar file generator

```
fab generate.jar
```
