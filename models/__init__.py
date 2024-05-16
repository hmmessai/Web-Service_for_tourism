#!/usr/bin/python3
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('DB_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.filestorage import FileStorage
    storage = FileStorage('instance/storage/file.json')

print('using storage of type: ' + storage.__class__.__qualname__)
storage.reload()
