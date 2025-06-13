from .expenses import expense_bp
from .export import export_bp
from .summary import summary_bp
from .auth import auth_bp

def register_routes(app):
    app.register_blueprint(expense_bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(auth_bp)