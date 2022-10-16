"""
Tuxbot core module: config

Contains all config workers
"""
import importlib
import os


config = importlib.import_module(os.environ["SETTINGS_MODULE"])
