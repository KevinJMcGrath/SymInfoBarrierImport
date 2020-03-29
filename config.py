import jsonpickle

from pathlib import Path

config_path = Path("./config.json")

with open(config_path, 'r') as _config_file:
    _config = jsonpickle.decode(_config_file.read())

bot_config = _config['bot_config']
app_config = _config['app_config']
obo_config = _config['obo_config']

