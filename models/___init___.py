#!/usr/bin/python3
"""Initialization of the package"""
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
