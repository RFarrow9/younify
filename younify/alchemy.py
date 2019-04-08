import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import pyodbc
"""
This file handles the database interactions

Currently the database is a hosted azure instance

Question remains is how this can be sharded?

Should each user only be able to see their own information?
Should we 'cache' information for users to shortcut computation? How often would this change?
How would we define a user? Could we do it by unique spotify user??
"""

conn = "mssql+pyodbc://rfarrow:sWEz7vdyDXjr@younify.database.windows.net/younify?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn)
engine.connect()

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    new = Column(String)

class Song(Base):
    __tablename__ = "Songs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    playlist_id = Column(Integer, ForeignKey(Playlist.id)) # Can be null, if populated, must exist in Playlists table
    album_id = Column(Integer, ForeignKey(Album.id)) # Can be null, if populated, must exist in Albums table
    title = Column(String)
    # Other song attribs here
    user = relationship(User, backref=backref('user', uselist=False))
    playlist = relationship(Playlist, backref=backref('playlist', uselist=False))


class Playlist(Base):
    __tablename = "Playlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    # Playlist attributes here
    user = relationship(User, backref=backref('user', uselist=False))


class Album(Base):
    __tablename__ = "Albums"
    id = Column(Integer, primary_key=True)

class Audiobook(Base):
    __tablename__ = "Audiobooks"
    id = Column(Integer, primary_key=True)




Base.metadata.create_all(engine)