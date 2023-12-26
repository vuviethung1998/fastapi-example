from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from server.database.sqlalchemy import Base



class Post(Base):
    __tablename__ = "items"

    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    post_content = Column(String, index=True)
    ticker = Column(String, ForeignKey("company.ticker"))

    # owner = relationship("User", back_populates="posts")