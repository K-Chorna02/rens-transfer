
from flask import render_template, Blueprint, url_for, redirect, flash, current_app, abort
from app.forms import LoginForm, UploadForm
from app.models import Graph
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required
from jinja2 import TemplateNotFound


main_bp = Blueprint('main', __name__)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    graph_list = [g for g in Graph.query.all()]

    return render_template('dashboard.html',graph_list = graph_list)


"""
@main_bp.route('/dashboard/<graph_id>')
def graph_endpoint(graph_id):
    
    g = Graph.query.get_or_404(int(graph_id))

    
    
    if not current_user.is_authenticated:
        if not g.public:
            abort(403)
    #graph_json = json.dumps(g.data)
    
    name = g.name
    try:
        return render_template(f'{name}.html')
    except TemplateNotFound:
        abort(404)"""

@main_bp.route('/graph_tester')
def graph_tester():
    return render_template('Line.html')





@main_bp.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():

        f = form.file_field.data
        filename = secure_filename(f.filename)
        destination_dataset = form.destination.data
        current_app.logger.info(f"Form validated successfully with {filename} and {destination_dataset}")
        
        if not current_app.testing:
            f.save(os.path.join(os.path.join(os.getcwd(), 'app/uploads', filename)))
            flash(f'Your file {filename} was uploaded',category='info')
        flash(f'File {filename} would be saved to {destination_dataset} in a non-testing environment.',category='warning')
        return redirect(url_for('main.index'))
    
    current_app.logger.info(f"choice field {form.destination.data}")
    return render_template('upload.html', form=form)



@main_bp.route('/')
def index():
    graph_list = Graph.query.filter_by(public=True).all()
    return render_template('index.html', graph_list=graph_list)


@main_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!',category='info')
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        form_password = form.password.data

        admin_user = current_app.config['ADMIN_USER']

        admin_hash = admin_user.password_hash
        admin_username = admin_user.username
        if username != admin_username or not check_password_hash(admin_hash,form_password):
            flash('Invalid username or password',category='error')
            return redirect(url_for('main.login'))
        
        login_user(admin_user,remember=form.remember_me.data)
        current_app.logger.info("Logged in admin")
        flash('Logged in successfully.',category='info')
        return redirect(url_for('main.index'))
    
    return render_template('login.html', form=form)


@main_bp.route('/logout')
def logout():
    logout_user()
    flash("Successfully logged out.", category='info')
    current_app.logger.info("Logged out admin")
    return redirect(url_for('main.index'))

@main_bp.route('/internal-error')
def internal_error():
    return render_template('does not exist.html')