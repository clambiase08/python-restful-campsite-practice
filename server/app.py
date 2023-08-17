from datetime import datetime

from flask import Flask, abort, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Campsite, Park, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Note: `app.json.compact = False` Configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Parks(Resource):
    def get(self):
        parks = [park.to_dict() for park in Park.query.all()]
        return make_response(parks, 200)


api.add_resource(Parks, "/parks")


class ParkById(Resource):
    def get(self, id):
        park = Park.query.get_or_404(id).to_dict()
        # park = Park.query.filter_by(id=id).first().to_dict()
        return make_response(park, 200)

    def patch(self, id):
        data = request.get_json()
        park = Park.query.get_or_404(id)
        for attr, value in data.items():
            setattr(park, attr, value)
        db.session.add(park)
        db.session.commit()
        return make_response(park.to_dict(), 202)

    def delete(self, id):
        park = Park.query.get_or_404(id)
        db.session.delete(park)
        db.session.commit()
        return make_response("", 204)


api.add_resource(ParkById, "/parks/<int:id>")


class Campsites(Resource):
    def get(self):
        campsites = [site.to_dict() for site in Campsite.query.all()]
        return make_response(campsites, 200)

    def post(self):
        data = request.get_json()
        # new_site = Campsite(
        #     max_capacity=data["max_capacity"],
        #     type=data["type"],
        #     site_fee=data["site_fee"],
        #     has_water=data["has_water"],
        #     has_bathroom=data["has_bathroom"],
        #     has_grill=data["has_grill"],
        #     park_id=data["park_id"],
        # )
        new_site = Campsite(**data)
        db.session.add(new_site)
        db.session.commit()
        return make_response(new_site.to_dict(), 201)


api.add_resource(Campsites, "/campsites")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
