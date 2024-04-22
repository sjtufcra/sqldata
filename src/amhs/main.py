import os 
import json
from typing import Dict,Any

#  From custom modules
from read_yaml import * 
from config import *
from create import *
from loguru import logger as log


def main():
    log.add(logPath,level=logLevel,retention=logDay)
    path = os.path.abspath(configpath)
    config = read_yaml_config(path)
    db = CreateDB(config)
    log.info('create db')
    return db,config
    # create_db(config)

def infer_mysql_type(value):
    if value is None:
        return 'VARCHAR(500)'
    elif isinstance(value, int):
        return 'INT'
    elif isinstance(value, float):
        return 'FLOAT'
    elif isinstance(value, str):
        return 'VARCHAR(255)'
    else:
        raise ValueError('Unsupported data type')
def get_json_file(db,dbname,path,tablename):
    filepath = os.path.abspath(path)
    with open(filepath,'r') as f:
        data = json.load(f)
    flag = tablename.split('_')
    index = f'{flag[0]}_{flag[1]}'

    filedata = data[index.upper()]
    for k,v in enumerate(filedata):
        if k == 0 and v is not None:
            create_table(db=db,dbname=dbname,data=v,name=tablename)
            db.connect()
        update_table(db,dbname,v,tablename)

def create_table(db,dbname,data,name):
    value = []
    for key,val in data.items():
        value.append(f'`{key}` {infer_mysql_type(val)}')
    db.connect()
    db.create_table(dbname,name,value)

def update_table(db,dbname,data,name):
    if data is None:
        log.info('data is None')
        return
    db.update_table(dbname,name,data)
    


if __name__ == '__main__':
    
    db,config = main()
    daname = config.mysql_database['database']
    db.create_db(daname)
    # create table to db    
    for key, path in enumerate(pathArray):
        if path.endswith('.json'):
            ph = os.path.abspath(path)
            get_json_file(db,daname,ph,config.mysql_database['table_names'][key])
    