
from importlib import resources
from pathlib import Path






class config:
    with resources.path("FinCarawler", 'resources') as _path_resource:
        PATH_RESOURCE = _path_resource



CONFIG = config()



