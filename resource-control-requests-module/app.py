from flask import Flask, redirect, url_for
from models import db
import config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['TESTING'] = config.TESTING

    db.init_app(app)

    from routes.employee import employee_bp
    from routes.manager import manager_bp

    app.register_blueprint(employee_bp)
    app.register_blueprint(manager_bp)

    @app.route('/')
    def index():
        return redirect(url_for('employee.list_requests'))

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
