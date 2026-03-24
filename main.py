from app import create_app, db
from sqlalchemy import inspect
from app.models import Graph
from app.db_init import populate_db,empty_db,create_generator_dict

application = create_app()

@application.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

def init_db():
    with application.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        graph_table_exists = inspector.has_table("graph")
        if not graph_table_exists:
            application.logger.info('Graph table missing after create_all(); skipping initial graph query')
            populate_db(create_generator_dict(), db)
            return

        if graph_table_exists and not Graph.query.first():
            populate_db(create_generator_dict(), db)
            application.logger.info('Graph table empty: populated dashboard graphs')

        if application.config['TESTING']:
            empty_db(db)
            populate_db(create_generator_dict(), db)
            application.logger.info('Testing mode: emptied and repopulated dashboard graphs')

if __name__ == '__main__':
    init_db()
    application.run(debug=application.config['TESTING'])