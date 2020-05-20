import yaml
from types import SimpleNamespace

def getParams(fileName):
    with open(fileName) as file:
        return yaml.full_load(file)