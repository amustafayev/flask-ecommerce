from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from src import app, db
from src.models import User, Item, Category, ContactDetails, Comment
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request


class UserModelView(ModelView):
    column_display_all_relations = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == app.config[
            'ADMIN_USERNAME']  # Only username test can have administration priviliges

    def inaccessible_callback(self, name, **kwargs):
        flash("Please Login with administrator user in order to continue", category="warning")
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))


class ItemAdmin(ModelView):
    form_columns = ['name', 'main_price', 'discount_price',
                    'description', 'user_id', 'image_path', 'category_id', 'comments']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == app.config[
            'ADMIN_USERNAME']  # Only username test can have administration priviliges

    def inaccessible_callback(self, name, **kwargs):
        flash("Please Login with administrator user in order to continue", category="warning")
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))


class CategoryAdmin(ModelView):
    form_columns = ['name', 'items']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == app.config[
            'ADMIN_USERNAME']  # Only username test can have administration priviliges

    def inaccessible_callback(self, name, **kwargs):
        flash("Please Login with administrator user in order to continue", category="warning")
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))


class CustomModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == app.config[
            'ADMIN_USERNAME']  # Only username test can have administration priviliges

    def inaccessible_callback(self, name, **kwargs):
        flash("Please Login with administrator user in order to continue", category="warning")
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))


admin = Admin(app, name='Admin Page', template_mode='bootstrap3')

admin.add_view(UserModelView(User, db.session))
admin.add_view(ItemAdmin(Item, db.session))
admin.add_view(CategoryAdmin(Category, db.session))
admin.add_view(CustomModelView(ContactDetails, db.session))
admin.add_view(CustomModelView(Comment, db.session))
