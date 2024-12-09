from sqlalchemy import Column, Integer, String, ForeignKey
from models.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    strength = Column(Integer, default=1)
    intelligence = Column(Integer, default=1)
    skin_color = Column(String(50), default="Unknown")
    hair = Column(String(50), default="Unknown")
