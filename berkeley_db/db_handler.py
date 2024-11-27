from dataclasses import dataclass, asdict
import threading
import bsddb3 as bsddb
import orjson
from typing import Dict


class BerkeleyDB:
    def __init__(self, db_path="/persistent/volumes/db") -> None:
        self.lock = threading.Lock()
        self.db_path = db_path
        # Create a database environment
        self.env = bsddb.db.DBEnv()
        self.start_database()
        self.opened_collections = {}

        self.running = True

    def start_database(self):
        with self.lock:
            self.env.open(
                f"{self.db_path}/env", bsddb.db.DB_CREATE | bsddb.db.DB_INIT_MPOOL
            )

    def get_collection(self, collection_name: str):
        if not self.running:
            return None

        with self.lock:
            if collection_name in self.opened_collections:
                return self.opened_collections[collection_name]
            else:
                _collection = bsddb.db.DB(self.env)
                _collection.open(
                    collection_name, None, bsddb.db.DB_HASH, bsddb.db.DB_CREATE
                )
                self.opened_collections[collection_name] = _collection
                return _collection

    def close(self):
        self.running = False
        with self.lock:
            for collection_name in self.opened_collections:
                self.opened_collections[collection_name].close()
            self.env.close


class IdGenerator:
    def __init__(self, db: BerkeleyDB, collection_name: str) -> None:
        self.lock = threading.Lock()
        self.db = db
        self.id_generator_collection = self.db.get_collection("id-generator")
        self.key_collection_name = orjson.dumps(collection_name)

    @property
    def next_id(self):
        with self.lock:
            curr_id = self.id_generator_collection.get(self.key_collection_name)
            if curr_id is None:
                collection_value = 0
            else:
                collection_value = orjson.loads(curr_id)
            collection_value += 1
            self.id_generator_collection.put(
                self.key_collection_name, orjson.dumps(collection_value)
            )
            return collection_value


class Model:
    def __init__(self, db: BerkeleyDB) -> None:
        self.db = db
        self.id_generator = IdGenerator(db, self.table_name)

    @property
    def table_name(self):
        return self.__class__.__name__

    @property
    def table(self):
        return self.db.get_collection(self.table_name)

    def save(self, key, obj):
        obj_json = asdict(obj)
        self.table.put(orjson.dumps(key), orjson.dumps(obj_json))

    def get(self, key):
        return self.table.get(orjson.dumps(key))


class VideoFileStreamsModel(Model):
    def __init__(self, db: BerkeleyDB) -> None:
        super().__init__(db)

    @dataclass
    class VideoFileStream:
        id: int = 0
        file_path: str = ""
        stream_path: str = ""
        video_options = {}
        stream_options = {}


def main():
    db = BerkeleyDB()

    vfs_model = VideoFileStreamsModel(db)

    id = vfs_model.id_generator.next_id
    vfs = vfs_model.VideoFileStream(
        id=id, file_path="/video", stream_path=f"mocked_stream_{id}"
    )
    vfs_model.save(vfs.file_path, vfs)

    value = vfs_model.get(vfs.file_path)
    print(value)


if __name__ == "__main__":
    main()
