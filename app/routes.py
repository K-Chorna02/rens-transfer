from flask import render_template, Blueprint, url_for, redirect, flash, current_app, abort
from app.forms import LoginForm, UploadForm
from app.models import Graph
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required
from jinja2 import TemplateNotFound

import pandas as pd
from app.data_validation import validate_df
from app.data_cleaning import clean_df


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = current_app.config['ADMIN_USER']
        if form.username.data == user.username and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)


@main_bp.route('/logout')
def logout():
    logout_user()
    flash("Successfully logged out.", category='info')
    current_app.logger.info("Logged out admin")
    return redirect(url_for('main.index'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    graph_list = [g for g in Graph.query.all()]
    return render_template('dashboard.html', graph_list=graph_list)


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        f = form.file_field.data
        destination_dataset = form.destination.data
        safe_filename = secure_filename(f.filename)

        current_app.logger.info(f"Upload received: {safe_filename} -> {destination_dataset}")

        try:
            raw_paths = {
                'activities': os.path.join(os.getcwd(), f'app/datasets/raw/Activities_raw{os.path.splitext(safe_filename)[1].lower()}'),
                'organisations': os.path.join(os.getcwd(), f'app/datasets/raw/Organisations_raw{os.path.splitext(safe_filename)[1].lower()}'),
                'meetings': os.path.join(os.getcwd(), f'app/datasets/raw/Meetings_raw{os.path.splitext(safe_filename)[1].lower()}'),
            }

            processed_paths = {
                'activities': os.path.join(os.getcwd(), 'app/datasets/processed/Activities_processed.csv'),
                'organisations': os.path.join(os.getcwd(), 'app/datasets/processed/Organisations_processed.csv'),
                'meetings': os.path.join(os.getcwd(), 'app/datasets/processed/Meetings_processed.csv'),
            }

            raw_path = raw_paths.get(destination_dataset)
            destination_path = processed_paths.get(destination_dataset)

            if not raw_path or not destination_path:
                flash('Invalid dataset selected.', category='error')
                return redirect(url_for('main.upload'))

            os.makedirs(os.path.dirname(raw_path), exist_ok=True)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            f.save(raw_path)
            current_app.logger.info(f'Saved raw upload to: {raw_path}')

            if raw_path.lower().endswith('.csv'):
                df = pd.read_csv(raw_path, dtype=str, engine='python', on_bad_lines='warn')
            elif raw_path.lower().endswith('.xlsx'):
                df = pd.read_excel(raw_path, dtype=str)
            else:
                raise ValueError('Unsupported file type')

            is_valid, errors = validate_df(df, destination_dataset)
            if not is_valid:
                form.file_field.errors.append(errors)
                return render_template('upload.html', form=form)

            cleaned_df = clean_df(df, destination_dataset)
            cleaned_df.to_csv(destination_path, index=False)

            current_app.logger.info(f'Saved cleaned CSV to: {destination_path}')

            from app.db_init import regenerate_graphs
            from app import db
            regenerate_graphs(db)

            flash('File uploaded and graphs updated successfully.', category='info')
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            current_app.logger.exception("Upload failed")
            form.file_field.errors.append(f"Error processing file: {str(e)}")

    return render_template('upload.html', form=form)


@main_bp.route('/graph_tester')
def graph_tester():
    return render_template('Line.html')


@main_bp.route('/internal-error')
def internal_error():
    return render_template('does not exist.html')
