from yaml import safe_load as load

from typing import Any

class DictAsObject:
    def __init__(self, dictionary: dict):
        for key, value in dictionary.items():
            setattr(self, key, value)
            # if isinstance(value, dict):
            #     setattr(self, key, DictAsObject(value))
            # else:
            #     setattr(self, key, value)

    def __getattr__(self, item: str) -> Any:
        try:
            return getattr(self, item)
        except AttributeError:
            pass

        keys = item.split('.')
        current_obj = self
        for key in keys:
            current_obj = getattr(current_obj, key)
            if current_obj is None:
                break

        if current_obj is None:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

        return current_obj

    def __setattr__(self, key: str, value: Any) -> None:
        if '.' in key:
            keys = key.split('.')
            current_obj = self
            for k in keys[:-1]:
                current_obj = getattr(current_obj, k)
            setattr(current_obj, keys[-1], value)
        else:
            super().__setattr__(key, value)
def read_yaml_config(file_path):
    with open(file_path, 'r') as f:
        config = load(f)
    return DictAsObject(config)