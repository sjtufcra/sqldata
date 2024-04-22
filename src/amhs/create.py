from mysql import connector
from loguru import logger as log
class CreateDB:
    def __init__(self,config):
        self.config = config.mysql_connection
        self.database = config.mysql_database
        self.conn = None
        self.cursor = None
        self.connflag = False
        self.connect()
    
    # connect to mysql
    def connect(self):
        self.conn = connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        self.connflag = True
        log.info("connect to mysql success")

    # create database
    def create_db(self,name):
        if name is None:
            log.info("database name is None")
            return
        if self.connflag:
            self.cursor.execute("""
                CREATE DATABASE IF NOT EXISTS {name}""")
            self.conn.commit()
            self.conn.close()
            log.info("create database success")
    # create user
    def create_user(self,name,password):
        if name is None or password is None:
            log.info("user name or password is None")
            return
        if self.connflag:
            self.cursor.execute("""
                CREATE USER IF NOT EXISTS {name} IDENTIFIED BY {password}""")
            self.conn.commit()
            self.conn.close()
            log.info("create user success")
            return
    # create table   
    def create_table(self,name,table_name,table_data):
        if name is None or table_name is None or table_data is None:
            log.info("database name or table name or table data is None")
            return
        if self.connflag:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {name}.{table_name} ({', '.join(table_data)})")
            self.conn.commit()
            self.conn.close()
            log.info("createtable success")
            return
    # update table
    def update_table(self,name,table_name,table_data):
        if name is None or table_name is None or table_data is None:
            log.info("database name or table name or table data is None")
            return
        if self.connflag:
            insert_query = f"INSERT INTO {table_name} ({', '.join(table_data.keys())}) VALUES ({', '.join(['%s'] * len(table_data))})"
            values = tuple(table_data.values())
            self.cursor.execute(insert_query,values)
            self.conn.commit()
            self.conn.close()
            log.info("update table success")
            return
        