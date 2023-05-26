from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from src import app, db
from src.forms import RegisterForm, LoginForm, ContactForm
from src.models import User, Item, Category, ContactDetails


@app.route("/<int:category_id>")
@app.route("/")
def home_page(category_id=None):
    if category_id is not None:
        items = Category.query.get_or_404(category_id).items
    else:
        items = Item.query.all()
    categories = Category.query.all()
    return render_template("home.html", products=items, categories=categories)


@app.route("/register", methods=['GET', 'POST'])
def register():
    print("Register endpoint start")
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    print("Register endpoint end")
    return render_template('register.html', form=form)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_detail = ContactDetails(name=form.name.data,
                                        email_address=form.email_address.data,
                                        subject=form.subject.data,
                                        message=form.message.data,
                                        )
        db.session.add(contact_detail)
        db.session.commit()
        flash("Contact Information Successfully sent", category="success")
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with sending contact information: {err_msg}', category='danger')
    return render_template("contact.html", form=form)


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(f'You have been logged out!', category='success')
    return render_template("logout.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password are incorrect! Please try again', category='danger')
            print("Incorrect username pass")
    return render_template("login.html", form=form)


@app.route("/items/<int:item_id>/favorite")
@login_required
def add_to_favorite(item_id):
    user = User.query.get_or_404(current_user.id)
    item = Item.query.get_or_404(item_id)
    if item in user.favorites:
        flash(f'Item {item.name} already is in favorites', category='warning')
    else:
        user.favorites.append(item)
        db.session.commit()
        flash(f'Item {item.name} successfully added to favorites', category='success')
    return redirect(url_for('item_detail', item_id=item_id))


@app.route("/items/<int:item_id>/favorite/remove")
@login_required
def remove_from_favorite(item_id):
    user = User.query.get_or_404(current_user.id)
    item = Item.query.get_or_404(item_id)
    if item not in user.favorites:
        flash(f'Item {item.name} is not in favorites', category='warning')
    else:
        user.favorites.remove(item)
        db.session.commit()
        flash(f'Item {item.name} successfully removed from favorites', category='success')
    return redirect(url_for("favorite_list", products=user.favorites))


@app.route("/favorite/items")
@login_required
def favorite_list():
    user = User.query.get(current_user.id)
    return render_template("favorites.html", products=user.favorites)


@app.route("/items/<int:item_id>")
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template("detail.html", product=item,
                           suggestions=filter(lambda suggestion: suggestion.id != item.id,
                                              Category.query.get_or_404(item.category_id).items
                                              )
                           )


@app.errorhandler(401)
def custom_401(error):
    flash(f'You need to login to continue!', category='danger')
    return redirect(url_for('login'))


@app.errorhandler(404)
def custom_401(error):
    return render_template("not_found.html")
