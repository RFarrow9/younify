from younify import *
from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine, MetaData


"""
This file handles the database interactions

Currently the database is a hosted azure instance

How can this be sharded/Horizontal partitioning?
Bring through the dates correctly.
Should each user only be able to see their own information?
Should we 'cache' information for users to shortcut computation? How often would this change?
How would we define a user? Could we do it by unique spotify user??

TODO: We really should use Django ORM
"""


engine = create_engine(database_connection)
Base = declarative_base()
session = sessionmaker()
session.configure(bind=engine)
log = motley.setup_logger(__name__)
database_connected = False

try:
    engine.connect()
    database_connected = True
except:
    log.warning("The database engine has failed to connect")
    log.info("Processing info will be written to local files, and attempts will be made at a later point to update database.")
    database_connected = False


def DropAllTables():
    meta = MetaData(engine)
    meta.reflect()
    meta.drop_all()


def AddTestUser():
    log.debug("Adding test user to database")
    testuser = User()
    testuser.name = "Test"
    testuser.fullname = "Test_User"
    testuser.nickname = "testyuser"
    testuser.new = "fsubv"
    #testuser.insert_dt = datetime.now()
    s = session()
    s.add(testuser)
    s.commit()


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    new = Column(String)
   #created = Column(datetime)


class Playlist(Base):
    __tablename__ = "Playlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    url = Column(String)
    title = Column(String)
    song_count = Column(Integer)
    #created = Column(datetime, default=datetime.utcnow)
    # Playlist attributes here
    # Relationships below here
    user = relationship(User, backref=backref('user', uselist=False))


class Album(Base):
    __tablename__ = "Albums"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    #created = Column(datetime, default=datetime.utcnow)
    # Album attributes here


class Audiobook(Base):
    __tablename__ = "Audiobooks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
   # created = Column(datetime, default=datetime.utcnow)
    # Audiobook attributes here


class Song(Base):
    __tablename__ = "Songs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    playlist_id = Column(Integer, ForeignKey(Playlist.id))  # Can be null, if populated, must exist in Playlists table
    album_id = Column(Integer, ForeignKey(Album.id))  # Can be null, if populated, must exist in Albums table
    url = Column(String)
    title = Column(String)
    artist = Column(String)
    found = Column(String)
    artist_id = Column(String)
    song_id = Column(String)
    user = relationship(User, backref=backref('song', uselist=False))
    playlist = relationship(Playlist, backref=backref('playlist', uselist=False))
 #   created = Column(datetime, default=datetime.utcnow)


def prime():
    DropAllTables()
    Base.metadata.create_all(engine)
    AddTestUser()


def main():
    print("This is not the entry point. Either run unittests, or run entry.py")


if __name__ == '__main__':
    main()
