from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Category, Item
import datetime

engine = create_engine('sqlite:///itemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

category1 = Category(name = 'Soccer')
session.add(category1)
session.commit()
item1 = Item(id = 1, name = 'Jersey', description = 'clothes for the players', category_name = 'Soccer', added = datetime.datetime.now())
item2 = Item(id = 2, name = 'Soccer cleats', description = 'shoes for the players', category_name = 'Soccer', added = datetime.datetime.now())
item3 = Item(id = 3, name = 'Soccer Ball', description = 'ball used to play', category_name = 'Soccer', added = datetime.datetime.now())
item4 = Item(id = 4, name = 'Shinguard', description = 'shinguard for protecting the legs', category_name= 'Soccer', added = datetime.datetime.now())

category2 = Category(name = 'Basketball')
session.add(category2)
session.commit()
item5 = Item(id = 5, name = 'Jersey', description = 'clothes for the players', category_name = 'Basketball', added = datetime.datetime.now())
item6 = Item(id = 6, name = 'Basketball Shoes', description = 'shoes for the players', category_name = 'Basketball', added = datetime.datetime.now())
item7 = Item(id = 7, name = 'BasketBall', description = 'ball used to play', category_name = 'Basketall', added = datetime.datetime.now())

category3 = Category(name = 'Baseball')
session.add(category3)
session.commit()
item8 = Item(id = 8, name = 'Jersey', description = 'clothes for the players', category_name = 'Baseball', added = datetime.datetime.now())
item9 = Item(id = 9, name = 'Baseball Shoes', description = 'shoes for the players', category_name = 'Baseball', added = datetime.datetime.now())
item10 = Item(id = 10, name = 'BaseBall', description = 'ball used to play', category_name = 'Baseball', added = datetime.datetime.now())
item11 = Item(id = 11, name = 'Bat', description = 'bat for hitting the ball', category_name = 'Baseball', added = datetime.datetime.now())
item12 = Item(id = 12, name = 'Gloves', description = 'gloves for catching the ball', category_name = 'Baseball', added = datetime.datetime.now())

category4 = Category(name = 'Frisbee')
session.add(category4)
session.commit()
item13 = Item(id = 13, name = 'Frisbee', description = 'Frisbee', category_name = 'Frisbee', added = datetime.datetime.now())

category5 = Category(name = 'Snowboarding')
session.add(category5)
session.commit()
item14 = Item(id = 14, name = 'Snowboard', description = 'board used to ski on snow', category_name = 'Snowboarding', added = datetime.datetime.now())
item15 = Item(id = 15, name = 'Googles', description = 'googles to protect the eyes', category_name = 'Snowboarding', added = datetime.datetime.now())

category6 = Category(name = 'Rock Climbing')
session.add(category6)
session.commit()
item16 = Item(id = 16, name = 'Rope', description = 'used for climbing', category_name = 'Rock Climbing', added = datetime.datetime.now())
item17 = Item(id = 17, name = 'Rock Climbing Showes', description = 'shoes for sticking on the rocks', category_name = 'Rock Climbing', added = datetime.datetime.now())

category7 = Category(name = 'Football')
session.add(category7)
session.commit()
item18 = Item(id = 18, name = 'Jersey', description = 'clothes for the players', category_name = 'Football', added = datetime.datetime.now())
item19 = Item(id = 19, name = 'Football Shoes', description = 'shoes for the players', category_name = 'Football', added = datetime.datetime.now())
item20 = Item(id = 20, name = 'FootBall', description = 'ball used to play', category_name = 'Football', added = datetime.datetime.now())

category8 = Category(name = 'Skating')
session.add(category8)
session.commit()
item21 = Item(id = 21, name = 'Skateboard', description = 'board for skating', category_name = 'Skating', added = datetime.datetime.now())
item22 = Item(id = 22, name = 'Knee pads', description = 'for protecting the knees', category_name = 'Skating', added = datetime.datetime.now())
item23 = Item(id = 23, name = 'Elbow pads', description = 'for protecting the elbows', category_name = 'Skating', added = datetime.datetime.now())
item24 = Item(id = 24, name = 'Helmet', description = 'for protecting the head', category_name = 'Skating', added = datetime.datetime.now())

category9 = Category(name = 'Hockey')
session.add(category9)
session.commit()
item25 = Item(id = 25, name = 'Jersey', description = 'clothes for the players', category_name = 'Hockey', added = datetime.datetime.now())
item26 = Item(id = 26, name = 'Hockey skates', description = 'shoes for the skiing', category_name = 'Hockey', added = datetime.datetime.now())
item27 = Item(id = 27, name = 'Puck', description = 'ball used to play', category_name = 'Hockey', added = datetime.datetime.now())
item28 = Item(id = 28, name = 'Strick', description = 'stick used to play', category_name = 'Hockey', added = datetime.datetime.now())
item29 = Item(id = 29, name = 'Helmet', description = 'for protecting the head', category_name = 'Hockey', added = datetime.datetime.now())

session.add(item1)
session.commit()

session.add(item29)
session.commit()

session.add(item2)
session.commit()

session.add(item28)
session.commit()

session.add(item3)
session.commit()

session.add(item27)
session.commit()

session.add(item4)
session.commit()

session.add(item26)
session.commit()

session.add(item5)
session.commit()

session.add(item25)
session.commit()

session.add(item6)
session.commit()

session.add(item24)
session.commit()

session.add(item7)
session.commit()

session.add(item23)
session.commit()

session.add(item8)
session.commit()

session.add(item22)
session.commit()

session.add(item9)
session.commit()

session.add(item21)
session.commit()

session.add(item10)
session.commit()

session.add(item20)
session.commit()

session.add(item11)
session.commit()

session.add(item19)
session.commit()

session.add(item12)
session.commit()

session.add(item18)
session.commit()

session.add(item13)
session.commit()

session.add(item17)
session.commit()

session.add(item14)
session.commit()

session.add(item16)
session.commit()

session.add(item15)
session.commit()

print ('all items added')
