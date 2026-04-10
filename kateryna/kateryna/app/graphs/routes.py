from app.graphs import bp
from app.models import Graph
from flask import abort,render_template, redirect, url_for, current_app
from flask_login import current_user
from app import db
from jinja2.exceptions import TemplateNotFound


@bp.route('/graph/<graph_id>')
def graph_endpoint(graph_id):
    if not graph_id:
        return redirect(url_for('main.dashboard'))
    try:
        id = int(graph_id)
        g = Graph.query.get(id)
        if g is None:
            return render_template('errors/basic404.html'), 404
    except ValueError as e:
        return render_template('errors/basic404.html'), 404
    
    if not current_user.is_authenticated:
        if not g.public:
            abort(403)
    
    name = g.name
    try:
        return render_template(f'graphs/{name}.html')
    except TemplateNotFound:
        print(f"Couldn't find graphs/{name}.html")
        abort(404)


@bp.route('/visibility/<graph_id>/<new_visibility>',methods=['GET','POST'])
def toggle_graph(graph_id=None, new_visibility=None):
    if not graph_id:
        abort(404)
    g = Graph.query.get(graph_id)

    if not g:
        abort(404)
    if not current_user.is_authenticated:
        abort(403)


    if new_visibility=='private':
        if not g.public:
            return "success", 200
        else:
            g.public = False
            db.session.commit()
            return "success",200
        
    elif new_visibility=='public':
        if g.public:
            return "success", 200
        else:
            g.public = True
            db.session.commit()
            return "success",200
    else:
        abort(404)
    


    
    