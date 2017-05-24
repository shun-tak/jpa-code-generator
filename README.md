# JPA entity generator

Java Persistence code generator, from existing MySQL tables to MySQL Schema, Entity and DAO.

- Reverse engineering existing MySQL tables into MySQL schema file (`fab generate.schema`)
- Generate Entity and DAO codes from MySQL schema file (`fab generate.entities`)

This generator is powered by [Python Fabric](http://www.fabfile.org/)


## Dependencies

- MySQL client 5.6 (mysql command)
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
env.mysql_user = "your_mysql_user_name"
env.mysql_database = "your_database_name"

env.schema_sql_dir = "src/main/resources/db/"
env.entity_dir = "src/main/java/path/to/entity"
env.entity_dao_base_dir = "src/main/java/path/to/entity/dao/base"
env.java_package_entity = "path.to.entity"
env.java_package_entity_dao_base = "path.to.entity.dao.base"
```

Create tables (migrate database):

```
# Run your DB migration tool (Flyway, Liquibase, etc.)
# or execute DDL (something like CREATE TABLE queries)
```

Run schema file generator:

```
cd jpa-entity-generator
fab generate.schema
```

Run entity file generator:

```
cd jpa-entity-generator
fab generate.entities
```
