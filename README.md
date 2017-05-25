# JPA entity generator

Java Persistence code generator, from existing MySQL tables to MySQL Schema, Entity and DAO.

- Reverse engineering existing MySQL tables into MySQL schema file (`fab generate.schema`)
- Generate jar package from MySQL schema file (`fab generate.jar`)
  - which contains Entities, JPA Metamodels and DAOs

This generator is powered by [Python Fabric](http://www.fabfile.org/)


## Dependencies

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
env.project_name = "example-entity"

env.mysql_host = "localhost"
env.mysql_user = "your_mysql_user_name"
env.mysql_database = "your_database_name"

env.schema_sql_dir = env.generated_dir + "/db"
env.persistence_xml_dir = env.generated_dir + "/src/main/resources/META-INF"
env.entity_dir = env.generated_dir + "/src/main/java/path/to/entity"
env.entity_dao_base_dir = env.generated_dir + "/src/main/java/path/to/entity/dao/base"
env.java_package_entity = "path.to.entity"
env.java_package_entity_dao_base = "path.to.entity.dao.base"
```

Run schema file generator:

```
cd jpa-entity-generator
fab generate.schema
```

Run jar package generator:

```
cd jpa-entity-generator
fab generate.jar
```
