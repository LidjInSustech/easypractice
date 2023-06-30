import json
import os

def read_config(filename):
    filename = os.path.join('configure', filename)
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

def write_config(filename, config):
    filename = os.path.join('configure', filename)
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)
    return config