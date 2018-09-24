from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))

    @property
    def serialize(self):
        return {
                "id": self.id,
                "name": self.name,
                "email": self.email
            }


class Category(Base):

    __tablename__ = 'category'
    name = Column(String(255), primary_key=True)

    @property
    def serialize(self):
        return {
                "name": self.name
            }


class Item(Base):

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    added = Column(DateTime)
    category_name = Column(String(255), ForeignKey('category.name'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(User)

    @property
    def serialize(self):
        return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "added": self.added,
                "category_name": self.category_name,
                "user": self.user_id
            }


engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.create_all(engine)
