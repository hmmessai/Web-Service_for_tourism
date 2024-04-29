#!/usr/bin/python3
from models.engine.filestorage import FileStorage


storage = FileStorage('storage/file.json')
storage.reload()
