# Item Catalog

##### A web application that shows items based on multiple categories and handles data CRUD manipulation from authroized users

## Contents :
 - static
 - templates
 - clients_secrets.json
 - database_setup.py
 - fill_database.py
 - application.py
 - README.md
### static
A folder that contains the css files for the website
##### Contents:
- styles.css

### templates
A folder that contains the html files of the website
##### Contents:
- home.html
- items.html
- itemDestails.html
- login.html
- register.html
- addItem.html
- editItem.html
- deleteItem.html

### client_secrets.json
A json file containning the application information for communicating with google api

### database_setup.py
A python file for initializing the database file

### fill_database.py
A python file for filling the database with data

### application.py
The main server file that starts the website

### Running the website
- copy the project folder into the vagrant directory
- open the command line
- cd into the vm directory
- run the vm by using the command:
`vagrant up`
- cd into the itemCatalog directory by using the command:
`cd /vagrant/itemCatalog`
- run the database_setup file with the command:
`python database_setup.py`
- fill the database with data by running the fill_database file with the command:
`python fill_database.py`
- run the server of the website by running the application file with the command:
`python application.py`
- Open the browser and navigate to http://localhost:5000 to start the home page

### Prerequistes for the project
- install vagrant from https://www.vagrantup.com/
- install virtual box from https://www.virtualbox.org/
- clone the required vm from https://github.com/udacity/fullstack-nanodegree-vm