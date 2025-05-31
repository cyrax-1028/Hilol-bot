from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, ForeignKey
from datetime import datetime
from app.database.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)


class Qori(Base):
    __tablename__ = "qorilar"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    audios = relationship("Audio", back_populates="qori", cascade="all, delete-orphan")


class Surah(Base):
    __tablename__ = "surah"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    arabic_name = Column(String, nullable=False)
    total_ayath = Column(Integer)
    revelation_type = Column(String, nullable=False)

    audios = relationship("Audio", back_populates="surah")


class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_id = Column(String, nullable=False)
    surah_id = Column(Integer, ForeignKey("surah.id"))
    qori_id = Column(Integer, ForeignKey("qorilar.id"), nullable=False)

    qori = relationship("Qori", back_populates="audios")
    surah = relationship("Surah", back_populates="audios")
