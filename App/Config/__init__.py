import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sessions_dirPath = f"{basedir}/UserAgent/sessions/"


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
