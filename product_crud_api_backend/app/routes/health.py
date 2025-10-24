from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("Healt Check", "health", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    """Health check endpoint for service liveness."""
    # PUBLIC_INTERFACE
    def get(self):
        """Return a simple JSON indicating service health."""
        return {"message": "Healthy"}
