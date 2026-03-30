from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os



login = LoginManager()
login.login_view = 'main.login'
db = SQLAlchemy()
migrate = Migrate()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.models import User, Graph
    from app.db_init import populate_db,empty_db, create_generator_dict
    from app.users import user_list

    

    admin_user = User(user_list["1"]["username"])
    admin_user.set_hash(user_list["1"]["password_hash"])
    app.config['ADMIN_USER'] = admin_user

   
    from app.errors import error_bp
    app.register_blueprint(error_bp)

    from app.graphs import bp
    app.register_blueprint(bp)



    import logging
    from logging.handlers import RotatingFileHandler

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setLevel('INFO')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                          '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel('INFO')

    

    app.logger.info('App startup')
    
    
    @app.cli.command("reset-db")
    def reset_db():
        """Empty and repopulate the database."""
        with app.app_context():
            from app.db_init import populate_db, empty_db, create_generator_dict
            empty_db(db)
            populate_db(create_generator_dict(), db)
            print("Database cleared and repopulated.")
    
    @app.cli.command("regenerate-csv")
    def regenerate_csv():
        """Re-clean data from CSV files"""

        import pandas as pd
        import os
        from app.data_cleaning import clean_df

        raw_dir = app.config['RAW_CSV_FOLDER'] or os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'datasets/raw'
        )
        dest_dir = app.config['PROCESSED_CSV_FOLDER'] or os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'datasets/processed'
        )
        dataset_files = {
            'activities': 'Activities.csv',
            'organisations': 'Organisations.csv',
            'meetings': 'Meetings.csv',
        }

        for dataset_type, filename in dataset_files.items():
            input_path = os.path.join(raw_dir, filename)

            if not os.path.exists(input_path):
                print(f"Skipping {filename}, not found")
                continue
            df = pd.read_csv(input_path, dtype=str)
            cleaned_df = clean_df(df, dataset_type)
            output_filename = f"{dataset_type.capitalize()}_processed.csv"
            filepath = os.path.join(dest_dir, output_filename)
            cleaned_df.to_csv(filepath, index=False)
            print(f"DF saved to {filepath}")
        print(f"Finished. Processed data can be found at {dest_dir}")
    
    return app

from app import models






