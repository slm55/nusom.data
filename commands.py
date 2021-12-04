import click
from flask.cli import with_appcontext

from model import db, DiseaseType, Disease, Country, Discover, Users, PublicServant, Doctor, Specialize, Record, Department

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()