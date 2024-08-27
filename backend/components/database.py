import datetime
import time

from peewee import MySQLDatabase, Model
from peewee import IntegerField, CharField, TextField, DateTimeField, ForeignKeyField, BooleanField, TimestampField

from utils.nanoId import nano_id, nano_number_id
from config import DATABASE

db = MySQLDatabase('chatroom', **DATABASE.get('dev'))


class _BaseModel(Model):

    class Meta:
        database = db


class User(_BaseModel):
    id = CharField(max_length=32, default=nano_id, primary_key=True)
    username = CharField(unique=True, null=False)
    password = CharField(null=False)
    role = CharField(null=True)

if __name__ == '__main__':
    db.connect()
    if not User.table_exists():
        User.create_table()
    db.close()
