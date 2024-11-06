import yaml

def load_config_from_yaml():
    with open("app.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

class Config:
    yaml_config = load_config_from_yaml()
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{yaml_config["database"]["user"]}:{yaml_config["database"]["password"]}@{yaml_config["database"]["host"]}:{yaml_config["database"]["port"]}/{yaml_config["database"]["database"]}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
