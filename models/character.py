from sqlalchemy import Column, Integer, String, ForeignKey
from models.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    clas = Column(String(50), nullable=False)
    class_image = Column(String(255), nullable=False)
    race = Column(String(50), nullable=False)
    strength = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    constitution = Column(String(50), nullable=False)
    intelligence = Column(Integer, nullable=False)
    wisdom = Column(Integer, nullable=False)
    charisma = Column(Integer, nullable=False)
    skin_color = Column(String(50), nullable=False)
    hair = Column(String(50), nullable=False)
