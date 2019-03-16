from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Flask Setup
app = Flask(__name__)

# Database Setup
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# App routes with WEB responses
@app.route('/')
@app.route('/restaurants/')
def listRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html",
        restaurants = restaurants)


@app.route('/restaurant/new/', methods=["GET", "POST"])
def createRestaurant():
    if request.method == "POST":
        if request.form["name"] and "submitButton" in request.form:
            newRestaurant = Restaurant(name=request.form["name"])
            session.add(newRestaurant)
            session.commit()
            flash('"%s" added to the list!' % newRestaurant.name)
        return redirect(url_for("listRestaurants"))
    else:
        return render_template("createRestaurant.html")


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=["GET", "POST"])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        if request.form["name"] and "submitButton" in request.form:
            restaurant.name = request.form["name"]
            session.add(restaurant)
            session.commit()
            flash('"%s" was successfully updated.' % restaurant.name)
        return redirect(url_for("listRestaurants"))
    else:
        return render_template("editRestaurant.html",
            restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=["GET", "POST"])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        if "submitButton" in request.form:
            session.delete(restaurant)
            session.commit()
            flash('"%s" was deleted!' % restaurant.name)
        return redirect(url_for("listRestaurants"))
    else:
        return render_template("deleteRestaurant.html",
            restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def listMenuItems(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuitems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template("menuItems.html",
        restaurant = restaurant,
        menuitems = menuitems)


@app.route('/restaurant/<int:restaurant_id>/menuitem/new/', methods=["GET", "POST"])
def createMenuItem(restaurant_id):
    if request.method == "POST":
        if request.form["name"] and "submitButton" in request.form:
            menuitem = MenuItem(
                name=request.form["name"],
                restaurant_id=restaurant_id,
                price=request.form["price"],
                description=request.form["description"])
            if request.form.getlist("course"):
                menuitem.course=request.form["course"]
            session.add(menuitem)
            session.commit()
            flash('"%s" was added to the menu!' % menuitem.name)
        return redirect(url_for("listMenuItems", restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template("createMenuItem.html",
            restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menuitem/<int:menuitem_id>/edit/', methods=["GET", "POST"])
def editMenuItem(restaurant_id, menuitem_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == "POST":
        if request.form["name"] and "submitButton" in request.form:
            menuitem.name=request.form["name"]
            menuitem.price=request.form["price"]
            menuitem.description=request.form["description"]
            if request.form.getlist("course"):
                menuitem.course=request.form["course"]
            session.add(menuitem)
            session.commit()
            flash('"%s" was successfully updated.' % menuitem.name)
        return redirect(url_for("listMenuItems", restaurant_id = restaurant_id))
    else:
        return render_template("editMenuItem.html",
            restaurant = restaurant,
            menuitem = menuitem)


@app.route('/restaurant/<int:restaurant_id>/menuitem/<int:menuitem_id>/delete/', methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menuitem_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == "POST":
        if "submitButton" in request.form:
            session.delete(menuitem)
            session.commit()
            flash('"%s" was deleted!' % menuitem.name)
        return redirect(url_for("listMenuItems", restaurant_id = restaurant_id))
    else:
        return render_template("deleteMenuItem.html",
            restaurant = restaurant,
            menuitem = menuitem)


# App routes with JSON responses
@app.route('/restaurants/JSON/')
def listRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def listMenuItemsJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuitems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[menuitem.serialize for menuitem in menuitems])


@app.route('/restaurant/<int:restaurant_id>/menuitem/<int:menu_id>/JSON/')
def getMenuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


if __name__ == "__main__":
    app.secret_key = "g507TCfcJGcrBz#c49LD8#3f5*9vdq"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
