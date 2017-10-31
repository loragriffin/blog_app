import datetime
import os
import peewee
from playhouse.db_url import connect

DB = connect(
    os.environ.get(
        'DATABASE_URL',
        'postgres://localhost:5432/blog'
    )
)


class BaseModel (peewee.Model):
    class Meta:
        database = DB


class Author (BaseModel):
    name = peewee.CharField(max_length=60)
    twitter = peewee.CharField(max_length=60)
    about = peewee.CharField()

    def __str__(self):
        return self.name


class BlogPost (BaseModel):
    author = peewee.ForeignKeyField(Author, null=True)

    title = peewee.CharField(max_length=60)
    slug = peewee.CharField(max_length=50, unique=True)
    body = peewee.TextField()
    created = peewee.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.title
