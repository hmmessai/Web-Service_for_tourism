#!/usr/bin/python3
from models.engine.filestorage import FileStorage


storage = FileStorage('instance/storage/file.json')
storage.reload()
