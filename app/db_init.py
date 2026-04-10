#from app import db
from app.models import Graph
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pandas as pd
import os
from inspect import getmembers, isfunction

basedir = os.path.dirname(os.path.abspath(__name__))
def create_generator_dict(
    activities_filepath='app/datasets/processed/Activities_processed.csv',
    organisations_filepath='app/datasets/processed/Organisations_processed.csv',
    meetings_filepath='app/datasets/processed/Meetings_processed.csv'):
    
    full_gens = {}
    from app import activities_visuals
    print(getmembers(activities_visuals,isfunction))
    for f in getmembers(activities_visuals,isfunction):
        full_gens[f[0]] = (f[1],activities_filepath)

    from app import org_visuals
    for g in getmembers(org_visuals,isfunction):
        full_gens[g[0]] = (g[1],organisations_filepath)

    return full_gens

def generate_html(source_path,name,function):

    df = pd.read_csv(source_path)

    fig = function(df)

    file_location = os.path.join(os.getcwd(),'app/templates/graphs',f'{name}.html')

    fig.write_html(file_location,include_plotlyjs='cdn',config={'responsive':True})

    return file_location


#this will fill the database with graphs (only if it's already empty)
#It must be called inside a WITH statement of flask app context
def populate_db(generator_path_dict:dict,db:SQLAlchemy):
    """
    generator_path_dict should take the form {name: (generator-function,path)}
    """
    for name,(function,source_path) in generator_path_dict.items():
        if not Graph.query.filter_by(name=name).first():
            file_loc = generate_html(source_path,name,function)
            g = Graph(name=name,path=file_loc)
            print(f'Adding {g} to the db session')
            db.session.add(g)

    db.session.commit()
    print('DB committed')


#nuclear - clear graphs from db. FOR TESTING!
#Like populate_db, requires application context.
def empty_db(db:SQLAlchemy):
    db.session.execute(text('TRUNCATE TABLE GRAPH'))
    db.session.commit()
    print(f"Database cleared.")

def regenerate_graphs(db: SQLAlchemy):
    """
    Deletes all graph records from the DB, deletes their HTML files,
    then regenerates everything from the current processed CSVs.
    Call this inside a Flask app context after a new CSV has been saved.
    """
    # Step 1: delete all existing graph HTML files and DB records
    graphs = Graph.query.all()
    for graph in graphs:
        if os.path.exists(graph.path):
            os.remove(graph.path)
            current_app.logger.info(f'Deleted HTML file: {graph.path}')
        db.session.delete(graph)

    db.session.commit()
    current_app.logger.info('All graph records cleared from DB.')

    # Step 2: rebuild everything from the current CSVs
    generator_dict = create_generator_dict()
    populate_db(generator_dict, db)
    current_app.logger.info('Graphs regenerated successfully.')

