from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    url_for,
    flash
)
from flask import session as login_session
import datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Connect to Databand create database session
engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine


# check whether a user is logged in or not
def checkLogin():
    return login_session.get('name') is not None


# check whether a user is authenticated to manage an item or not
def checkAuthentication(category_name, item_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(name=login_session['name'],
                                         email=login_session['email']).first()
    item = session.query(Item).filter_by(user_id=user.id,
                                         name=item_name,
                                         category_name=category_name).first()
    if item is not None:
        return item.name == item_name
    else:
        return False


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render the login page on GET request
        return render_template('login.html', login_session=login_session,
                               client_id=CLIENT_ID)
    else:
        # Check the database for authorization on POST request
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if session.query(User).filter_by(name=request.form['name'],
                                         password=request.form['password']
                                         ).first() is None:
            # The authorization wasn't granted
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        else:
            # The authorization was successful and the user is logged in
            user = session.query(User).filter_by(name=request.form['name'],
                                                 password=request.form[
                                                     'password'
                                                     ]
                                                 ).first()
            login_session['name'] = user.name
            login_session['email'] = user.email
            flash('Logged In Successfully')
            return redirect(url_for('showCategories'))


# logout page
@app.route('/logout', methods=['POST'])
def logout():
    if login_session.get('access_token') is not None:
        # redirect to the gdisconnect page if the user signed in with google
        return redirect(url_for('gdisconnect'), code=307)
    # log the user out normally if he didn't sign in with google
    del login_session['name']
    flash('Logged Out Successfully')
    return redirect(url_for('showCategories'))


# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Render the register page on GET request
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return render_template('register.html', login_session=login_session)
    else:
        # Register the user on POST request
        # Validate the input data
        if request.form['name'] == "":
            flash('Please Enter Username')
            return render_template('register.html',
                                   login_session=login_session)
        elif request.form['password'] == "":
            flash('Please Enter Password')
            return render_template('register.html',
                                   login_session=login_session)
        elif request.form['email'] == "":
            flash('Please Enter Email')
            return render_template('register.html',
                                   login_session=login_session)
        elif request.form['password'] != request.form['cpassword']:
            flash("Passwords Don't Match")
            return render_template('register.html',
                                   login_session=login_session)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        user = User(name=request.form['name'],
                    password=request.form['password'],
                    email=request.form['email'])
        session.add(user)  # add user to database
        session.commit()
        return redirect(url_for('login'))  # reditect to login page


# login from google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['name'] = data['name']
    login_session['email'] = data['email']
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    if (session.query(User).filter_by(name=data['name'],
                                      email=data['email']).first() is None):
        user = User(name=data['name'], email=data['email'])
        session.add(user)
        session.commit()
    flash('Logged In Successfully')
    return "login successful"


# logout for google
@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = "https://accounts.google.com/o/oauth2/"
    url += "revoke?token=%s" % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['name']
        return redirect(url_for('showCategories'))
    else:
        response = make_response(json.dumps('Failed to revoke token.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash('Logged Out Successfully')
        return response


# Home page, viewing all categories
@app.route('/')
@app.route('/catalog')
def showCategories():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.added.desc()).limit(9).all()
    return render_template('home.html', categories=categories, items=items,
                           login_session=login_session)


# Item page, viewing all items of a certain category
@app.route('/catalog/<path:category_name>')
@app.route('/catalog/<path:category_name>/')
@app.route('/catalog/<path:category_name>/items')
def showItems(category_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_name=category_name).all()
    return render_template('items.html', categories=categories, items=items,
                           login_session=login_session)


# Item page, viewing item details
@app.route('/catalog/<path:category_name>/<path:item_name>')
@app.route('/catalog/<path:category_name>/<path:item_name>/')
def showItemDetails(category_name, item_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(name=item_name,
                                         category_name=category_name).one()
    return render_template('itemDetails.html', item=item,
                           login_session=login_session)


# Item page, add new item
@app.route('/catalog/<path:category_name>/items/add',
           methods=['GET', 'POST'])
def addItem(category_name):
    # checking if the user is logged in
    if checkLogin() is False:
        return redirect(url_for('login'))
    if request.method == 'GET':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        categories = session.query(Category).all()
        category = session.query(Category).filter_by(name=category_name).one()
        return render_template('addItem.html', categories=categories,
                               category=category,
                               login_session=login_session)
    else:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        usr = session.query(User).filter_by(name=login_session['name'],
                                            email=login_session['email']).one()
        item = Item(name=request.form['name'],
                    description=request.form['description'],
                    added=datetime.datetime.now(),
                    category_name=request.form['category'],
                    user_id=usr.id)
        session.add(item)
        session.commit()
        flash('New Item Added Successfully')
        return redirect(url_for('showItems', category_name=category_name))


# Item page, edit item
@app.route('/catalog/<path:category_name>/<path:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    # checking if the user is logged in
    if checkLogin() is False:
        return redirect(url_for('login'))
    if checkAuthentication(category_name, item_name) is False:
        flash("Sorry, you don't have permission to edit this item")
        return redirect(url_for('showItemDetails', category_name=category_name,
                        item_name=item_name))
    if request.method == 'GET':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        categories = session.query(Category).all()
        item = session.query(Item).filter_by(name=item_name,
                                             category_name=category_name).one()
        return render_template('editItem.html', categories=categories,
                               item=item, login_session=login_session)
    else:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(Item).filter_by(name=item_name,
                                             category_name=category_name).one()
        item.name = request.form['name']
        item.description = request.form['description']
        item.category_name = request.form['category']
        session.add(item)
        session.commit()
        flash('Item Editted Successfully')
        return redirect(url_for('showItems', category_name=category_name))


# Item page, delete item
@app.route("""/catalog/<path:category_name>/
           <path:item_name>/delete""", methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    # checking if the user is logged in
    if checkLogin() is False:
        return redirect(url_for('login'))
    if checkAuthentication(category_name, item_name) is False:
        flash("Sorry, you don't have permission to delete this item")
        return redirect(url_for('showItemDetails', category_name=category_name,
                        item_name=item_name))
    if request.method == 'GET':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(Item).filter_by(name=item_name,
                                             category_name=category_name).one()
        return render_template('deleteItem.html', item=item,
                               login_session=login_session)
    else:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(Item).filter_by(name=item_name,
                                             category_name=category_name).one()
        session.delete(item)
        session.commit()
        flash('Item Deleted Successfully')
        return redirect(url_for('showItems', category_name=category_name))


# JSON ENDPOINTS
@app.route('/catalog/api/JSON')
def categoriesJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    cats = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in cats])


@app.route('/catalog/<path:category_name>/items/api/JSON')
def itemsJSON(category_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(Item).filter_by(category_name=category_name)
    return jsonify(items=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'mykey'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
