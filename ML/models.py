import os

import joblib


def get_models_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")


def get_file_path(file_name):
    # return os.path.join(get_models_path(), file_name)
    return os.path.join("models", file_name)


def save_model(model, file_name):
    joblib.dump(model, get_file_path(file_name))


def load_model(file_name):
    return joblib.load(get_file_path(file_name))
