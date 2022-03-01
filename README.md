# MySQL Manager

## What is it:

MySQL Manager is a package to easily connect to a MySQL Schema and manager it.
I created it with personal purpose, using [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) and [pymysql](https://github.com/PyMySQL/PyMySQL) as backend.

## How to get it:

Currently this package is just available on Test PyPI, to get it you can use:

``` bash	
pip install -i https://test.pypi.org/simple/ mysqlmanager
```

Or clone this repository. :smile:

## What it do:

Actually this package has composed by just one module with a class where you can create a instance, for each schema/database on MySQL.

The functions in class do:

- Get the name of tables on selected schema
- Read a specific table and return
  - Name of columns (list format)
  - Values of tables (list format)
  - Entire table in _SQLAlchemy.Table_ format
  - And as selected table
- Insert new values to table

This package have a special group of functions that verify type of each column in table and if exist DATE format this will **try** to convert date string into ISOFormat, if other format is used.

## How to use:

### Import package

``` py
from mysqlmanager.manager import SQLManager
```

### To create a connection with Schema:

````py
local_db = SQLManager('user',
'password',
'schema')
````

### Functions in this class:

```py
# Get the name of all tables inside Schema
local_db.tables()

# Read a specific table
mytable = local_db.get_table('tablename')
```

Some available attributes:
```py
# Get columns name on table
mytable.columns

# Get values from table (fetchall)
mytable.values

# Return the table
mytable.table 

# Or
mytable.selected_table  
```

### To insert new values:

For use this function you need insert the value for each column in order into a list. 
*In future: you can use a dictionary*

#### Example - A table with columns ID, First Name, Last Name, Age, Sex, Birthday.

````py
values = ['01', 'Alexandre', 'Carrascosa', '99', 'Male', '1900-01-01']
local_db.insert('users', values)
````

## Author

Carrascosa, Alexandre.

## License

[MIT](https://choosealicense.com/licenses/mit/)