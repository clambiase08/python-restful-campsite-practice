from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Park(db.Model, SerializerMixin):
    __tablename__ = "parks"
    serialize_rules = ("-campsites.park",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String, nullable=False)
    entrance_fee = db.Column(db.Float)
    has_trails = db.Column(db.Boolean)
    has_RV_cleanout = db.Column(db.Boolean)
    begin_camping_season = db.Column(db.DateTime)
    end_camping_season = db.Column(db.DateTime)

    campsites = db.relationship("Campsite", backref="park", cascade="delete")

    @validates("entrance_fee")
    def validate_fee(self, key, entrance_fee):
        if not 13.99 < entrance_fee < 25:
            raise ValueError("Fee must be between $13.99 and $25")
        return entrance_fee

    def __repr__(self):
        return f"<Park: {self.name} | Address: {self.address}>"


class Campsite(db.Model, SerializerMixin):
    __tablename__ = "campsites"
    serialize_rules = ("-reservations.campsite",)

    id = db.Column(db.Integer, primary_key=True)
    max_capacity = db.Column(db.Integer)
    type = db.Column(db.String)
    site_fee = db.Column(db.Float)
    has_water = db.Column(db.Boolean)
    has_bathroom = db.Column(db.Boolean)
    has_grill = db.Column(db.Boolean)
    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))

    reservations = db.relationship("Reservation", backref="campsite", cascade="delete")

    @validates("max_capacity")
    def validate_capacity(self, key, capacity):
        if not capacity <= 10:
            raise ValueError("Max Capacity must be less than or equal to 10")
        return capacity

    @validates("type")
    def validate_type(self, key, type):
        if type != "tent" and type != "RV":
            raise ValueError("Invalid type")
        return type

    def __repr__(self):
        return f"<Campsite ID: {self.id} | type: {self.type} | capacity: {self.max_capacity}"


class Reservation(db.Model, SerializerMixin):
    __table_name__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    campsite_id = db.Column(db.Integer, db.ForeignKey("campsites.id"))

    @validates("start_date")
    def validate_start(self, key, start_date):
        if (
            not self.campsite.park.begin_camping_season
            < start_date
            < self.campsite.park.end_camping_season
        ):
            raise ValueError("Start date must be in the camping season")
        return start_date

    @validates("end_date")
    def validate_end(self, key, end_date):
        if (
            not self.campsite.park.begin_camping_season
            < end_date
            < self.campsite.park.end_camping_season
        ):
            raise ValueError("End date must be in the camping season")
        return end_date
