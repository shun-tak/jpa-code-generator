# JPA entity generator

Java Persistence code generator, from existing MySQL tables to MySQL Schema, Entity and DAO.

- Reverse engineering existing MySQL tables into MySQL schema file (`fab generate.schema`)
- Generate jar package from MySQL schema file (`fab generate.jar`)
  - which contains Entities, JPA Metamodels and DAOs

This generator is powered by [Python Fabric](http://www.fabfile.org/)

Generated codes are depend on Hibernate implementation for now.


## Dependencies

Dependencies for this generator, not for generated sources.

- MySQL client 5.6 (`mysqldump` command)
- Python 2.7
- fabric
- jinja2 (Python template module)


## Usage

Clone this repo:

```
git clone
```

Edit `env` in fabfile/\__init\__.py:

```
env.project_name = 'example-entity'

env.mysql_host = 'localhost'
env.mysql_user = 'your_mysql_user_name'
env.mysql_database = 'your_database_name'

env.entity_dir = env.java_source_dir + '/example/project/entity'
env.entity_dao_dir = env.java_source_dir + '/example/project/entity/dao'
env.java_package_entity = 'example.project.entity'
env.java_package_entity_dao = 'example.project.entity.dao'
```

Run schema file generator:

```
cd jpa-entity-generator
fab generate.schema
```

Run jar package generator with your build version:

```
cd jpa-entity-generator
fab generate.jar:<version>
```

e.g. `fab generate.jar:1.0.0-SNAPSHOT`
