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
    # create_db(config)
    pass

def infer_mysql_type(value):
    if value is None:
        return 'NULL'
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
    create_table(db=db,dbname=dbname,data=data,tablename=tablename)

def create_table(db,dbname,data,name):
    value = []
    for key,value in data.items():
        value.append(f'{key} {infer_mysql_type(value)}')
    db.create_table(dbname,name,value)

def update_table(db,dbname,data,name):
    if data is None:
        log.info('data is None')
        return
    db.update_table(dbname,name,data)
    


if __name__ == '__main__':
    main()