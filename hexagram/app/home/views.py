from flask import render_template, redirect, url_for, flash, request
from . import home

@home.route('/') # Route is the same as home page
@home.route('/home')
def home_page():
    """
    Loads home page
    """
    return render_template('home.html')

@home.route('/about')
def about_page():
    """
    Loads about page
    """
    return render_template('about.html')