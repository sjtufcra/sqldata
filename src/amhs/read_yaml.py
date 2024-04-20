import yaml

# read yaml config file
class DictAsObject:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

def read_yaml_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return DictAsObject(config)