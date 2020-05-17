import yaml
from types import SimpleNamespace

def getParams(fileName):
    with open(fileName) as file:
        return SimpleNamespace(**yaml.full_load(file))