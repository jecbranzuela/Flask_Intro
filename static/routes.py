from static import app, db
from flask import render_template, redirect, url_for, request,flash, get_flashed_messages
#import the classes from entities.py
from static.entities import *
import locale
from datetime import datetime
from static.forms import *
from flask_login import current_user, login_user,logout_user,login_required

@app.route('/')
@app.route('/main')
@login_required
def index():
    return redirect(url_for('search'))

@app.route('/search',methods=['GET', 'POST'])
@login_required
def search():
    query = request.args.get('query','')
    category = request.args.get('category', 'All')
    if category == 'Electronics':
        results = Electronics.query.filter(Electronics.name.ilike(f"%{query}%") | Electronics.id.ilike(f"%{query}%")).all()
    elif category == 'Clothing':
        results = Clothing.query.filter(Clothing.name.ilike(f"%{query}%") | Clothing.id.ilike(f"%{query}%")).all()
    elif category == 'Food':
        results = Food.query.filter(Food.name.ilike(f"%{query}%") | Food.id.ilike(f"%{query}%")).all()
    else:
        results = Item.query.filter(Item.name.ilike(f"%{query}%") | Item.id.ilike(f"%{query}%")).all()

    itemsFormatted = FormatItem(results)
    form = ElectronicsForm()
    return render_template('index.html', items=itemsFormatted, query=query,form=form,category=category)

@app.route('/register_electronics', methods=['GET', 'POST'])
def RegisterElectronics():
    form = ElectronicsForm()
    #[(client.id, f'{client.id}, {Client.getClientFullName(client.id)}') for client in clients]
    #form.type.choices

    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        manufacturer = form.manufacturer.data

        elec_to_create = Electronics(name=name, price=price,description=description,manufacturer=manufacturer)

        similarElectronics = Electronics.query.filter(Electronics.name.like(f'%{elec_to_create.name}')).all()
        if similarElectronics:
            flash(f'Item {elec_to_create.name} is already in the database!',category='warning')
        else:
            db.session.add(elec_to_create)
            db.session.commit()
            flash(f'Success! Item {elec_to_create.name} has been created!', category='success')
            query = request.args.get('query','')
            results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
            itemsFormatted = FormatItem(results)
            itemsFormatted = [itemsFormatted[-1]] + itemsFormatted[:-1]
            return render_template('index.html', items=itemsFormatted, query=query,form=form)
    
    FormError(form)
    return redirect(url_for('search'))

@app.route('/UpdateItem/<item_id>', methods=['GET', 'POST'])
def UpdateItem(item_id):
    ItemToUpdate = Item.query.filter_by(id=item_id).first()
    if ItemToUpdate.type == "electronics":
        form = ElectronicsForm(obj=ItemToUpdate)
    elif ItemToUpdate.type == "clothing":
        form = ClothingForm(obj=ItemToUpdate)
    elif ItemToUpdate.type == "food":
        form = FoodForm(obj=ItemToUpdate)
    if form.validate_on_submit():
        form.populate_obj(ItemToUpdate)
        db.session.commit()
        flash(f'Success! The update has been committed to the database', category='success')
        return redirect(url_for('index'))
    else:
        FormError(form)
    return render_template('UpdateItem.html',form=form,type=ItemToUpdate.type)

@app.route('/register_user', methods=['GET', 'POST'])
def RegisterUser():
    form = UserForm()
    if form.validate_on_submit():
        user_to_create = User(
            name=form.name.data,
            description = form.description.data,
            passwordHash = form.password1.data,
            birthDate = form.birthDate.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Success! User has been created!', category='success')
        return redirect(url_for('index'))
    else:
        FormError(form)
    return render_template('RegisterUser.html',form=form)

@app.route("/login", methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name=form.name.data).first()
        if attempted_user and attempted_user.checkPassword(attemptedPassword=form.password.data):
            login_user(attempted_user) 
            flash(f'Success. You are logged in as: {attempted_user.name}', category='success')
            return redirect(url_for('index'))
        else:
            flash('name and password does not exist in the database!',category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('index'))

'''
    Format the price with commas every three digits.
    In the locale.format_string() function in Python, the grouping parameter specifies whether 
    or not to include digit grouping separators in the formatted output. When grouping is set to True,
    it enables digit grouping, which means that the formatted string will include commas to separate groups of 
    digits according to the locale's grouping rules.


    Inside the search() route, we loop through the results and use strftime('%B %d, %Y') to format the date_purchased attribute. 
    %B represents the full month name (e.g., January, February, etc.), %d represents the day, and %Y represents the four-digit year.
'''
def FormError(form):
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')
def FormatItem(items):
    # Set the locale to use the user's default settings
    locale.setlocale(locale.LC_ALL,'')
    # month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for item in items:
        item.price = locale.format_string("%.2f", item.price, grouping=True)
        # month_number = item.datePurchased.month - 1  # Month numbers are zero-based in Python
        # month_name = month_names[month_number]
        # item.datePurchased = f"{month_name} {item.datePurchased.day}, {item.datePurchased.year}"
    return items