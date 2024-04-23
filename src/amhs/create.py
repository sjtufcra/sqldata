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
            self.cursor.execute(f"""
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
            val = ', '.join(table_data)
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}.{table_name} ({val})")
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
            values = []
            for key,val in table_data.items():
                values.append(f'`{key}`')
            keys = ', '.join(values)
            values_placeholders = ', '.join(['%s'] * len(table_data))
            insert_query = f"INSERT INTO {name}.{table_name} ({keys}) VALUES ({values_placeholders})"
            values = tuple(table_data.values())
            self.cursor.execute(insert_query,values)
            self.conn.commit()
            return
    
    # delete table
    def delete_table(self,name,table_name):
        if self.connflag:
            self.cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{name}' AND TABLE_NAME = '{table_name}'")
            table_exists = self.cursor.fetchone()[0]

            if table_exists > 0:
                delete_query = f"DROP TABLE {name}.{table_name}"
                self.cursor.execute(delete_query)
            self.conn.commit()
            self.conn.close()
            log.info(f"delete table success: {table_name}")
            return
    # show tables type 
    def show_tables(self,name,table_name):
        if self.connflag:
            query = f"DESCRIBE {name}.{table_name}"
            self.cursor.execute(query)
            typelist = []
            # 解析并打印字段类型
            for (column_name, data_type, _, _, _, _) in self.cursor:
                print(f"{column_name}: {data_type}")
                typelist.append(data_type)
            return typelist