import pymysql
import sqlalchemy as db
from dateutil.parser import parse
from datetime import datetime

from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker


class SQLManager:
    
    def __init__(self, user, password, schema):
        
        engine = create_engine(f'mysql+pymysql://{user}:{password}@127.0.0.1/{schema}')
        self.conn = engine.connect()
        self.exec = self.conn.execute
           
        self.Base = declarative_base()
        
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.metadata = MetaData()
        self.engine = engine
        self.insp = inspect(self.engine)
    
    def tables(self):
        '''
        OUTPUT:
            Return the name of all tables in Schema
        '''
        return self.insp.get_table_names()
    
    def get_table(self, tablename) -> db.Table:
        '''
        Read a specific table in Schema and select this.
        When used you can apply others functions to this instance.               
        
        INPUT:
            tablename (str): Name of table to read
            
        OUTPUT:
            Return the self function.
        '''
        assert isinstance(tablename, str), "You need put a string type with table name"
        
        table = db.Table(tablename,
                         self.metadata,
                         autoload = True,
                         autoload_with = self.engine)
        
        self.selected_table = db.select([table])
        self.columns = self.selected_table.columns.keys()
        self.values = self.exec(self.selected_table).fetchall()
        
        self.table = table
        
        return self
    
    def _is_date(self, string):
        '''
        This function verify if a string have a date format.
            
        INPUT:
            string (str): Text to verify
        
        OUTPUT:
            Boolean (False/True)
        '''
        
        try:
            parse(string, fuzzy=False)
            return True
        except ValueError:
            return False
        
    def _date_isoformat(self, string):
        '''
        Convert a string, with date format, into ISO Date Format (YYYY-MM-DD)
        
        INPUT:
            string (str): Date to convert
            
        OUTPUT:
            date (datetime): Date with Isoformat
        
        '''
        
        date = parse(string)
        return date.isoformat()
        
    
    def _verify_columns_type(self, table):
        '''
        Read all columns in dataframe, and return a list with type of each column.
        
        Example: 
        01 | "name" | 01/01/1900
        
        Will return a list like: [int, str, DATETIME]
        
        INPUT:
            table (pd.DataFrame): A pandas Dataframe
            
        OUTPUT:
            columns_type (list): A list with columns type
        '''
        columns_table = self.insp.get_columns(table)
        columns_type = []
        
        for column in columns_table:
            columns_type.append(str(column['type']))
        
        return columns_type

    def insert(self, table, values):
        '''
        This function insert values into columns to specified table
        INPUT:
            table (str): Name of table that you want acess
            values (list): List of values for any column in table
            
            --------------
            For datetime you need to insert data in ISOFORMAT (YYYY-MM-DD)
        '''
        
        assert isinstance(values, list), \
        'The values need be a list of values'
        
        db_table = self.get_table(table).table
        columns = self.get_table(table).columns
        columns_type = self._verify_columns_type(table)
        query = db.insert(db_table)
                
        try: 
            assert len(values) == len(columns)
        
        except:
            message = ('The length of values list need be the same of columns, '
            f'this table have {len(columns)} columns and your list '
            f'have {len(values)}!')
            raise ValueError(message)
            
        else:
            if 'DATE' in columns_type:
                date_index = columns_type.index('DATE')
                
                try:
                    self._is_date(values[date_index])
                    values[date_index] = self._date_isoformat(values[date_index])
                
                except:
                    message = ('This date format is invalid, please '
                               'insert a date like YYYY-MM-DD')
                    raise ValueError(message)
                
            else:
                    
              dict_of_values = dict(zip(columns, values))                
              insert_data = self.exec(query, dict_of_values)


    def disconnect(self):
        '''
        Close session and connections with DataBase
        '''
        self.conn.close()
        self.session.close()
        self.engine.dispose()
        
        
        
    
