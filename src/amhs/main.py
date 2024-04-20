import os 
from read_yaml import * 
from config import *

def main():
    path = os.path.abspath(configpath)
    config = read_yaml_config(path)