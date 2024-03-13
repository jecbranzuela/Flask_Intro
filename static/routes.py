from static import app, db
from flask import render_template, redirect, url_for, request,flash, get_flashed_messages
#import the classes from entities.py
from static.entities import Item, User
import locale
from datetime import datetime
from static.forms import *

@app.route('/')
@app.route('/main')
def index():
    return redirect(url_for('search'))

@app.route('/search',methods=['GET', 'POST'])
def search():
    query = request.args.get('query','')
    results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
    itemsFormatted = FormatItem(results)
    form = RegisterItemForm()
    return render_template('index.html', items=itemsFormatted, query=query,form=form)

@app.route('/register_item', methods=['GET', 'POST'])
def RegisterItem():
    form = RegisterItemForm()

    #[(client.id, f'{client.id}, {Client.getClientFullName(client.id)}') for client in clients]
    #form.type.choices
    if form.validate_on_submit():
        item_to_create = Item(
            name=form.name.data,
            price=form.price.data,
            #type = form.type.data,
            datePurchased=form.datePurchased.data
        )
        db.session.add(item_to_create)
        db.session.commit()
        flash('Success! Item has been created!', category='success')
        query = request.args.get('query','')
        results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
        itemsFormatted = FormatItem(results)
        itemsFormatted = [itemsFormatted[-1]] + itemsFormatted[:-1]
        return render_template('index.html', items=itemsFormatted, query=query,form=form)
    
    FormError(form)
    return redirect(url_for('search'))

@app.route('/UpdateItem/', methods=['GET', 'POST'])
def UpdateItem():
    item = request.form('item_id')
    ItemToUpdate = Item.query.get(item)
    form = RegisterItemForm(obj=ItemToUpdate)
    if form.validate_on_submit():
        form.populate_obj(ItemToUpdate)
        ItemToUpdate.name = form.name.data
        ItemToUpdate.price = form.price.data
        ItemToUpdate.datePurchased = form.datePurchased.data
        flash(f'Success! The update has been committed to the database', category='success')
        db.session.commit()
        return redirect(url_for('search'))






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
            flash(f'Error in creating a user: {err_msg}', category='danger')
def FormatItem(items):
    # Set the locale to use the user's default settings
    locale.setlocale(locale.LC_ALL,'')
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for item in items:
        item.price = locale.format_string("%.2f", item.price, grouping=True)
        month_number = item.datePurchased.month - 1  # Month numbers are zero-based in Python
        month_name = month_names[month_number]
        item.datePurchased = f"{month_name} {item.datePurchased.day}, {item.datePurchased.year}"
    return items