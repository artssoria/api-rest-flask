from flask import request, Blueprint

from flask_restful import Api, Resource
from ...common.error_handling import ObjectNotFound
from .schemas import FilmSchema
from ..models import Film, Actor

films_v1_0_bp = Blueprint('films_v1_0_bp', __name__)
film_schema = FilmSchema()


class FilmListResource(Resource):
    def get(self):
        films = Film.query.all()
        result = film_schema.dump(films, many=True)
        return result, 200
    def post(self):
        data = request.get_json()
        film_dict = film_schema.load(data)
        film = Film(title = film_dict['title'],
                    length = film_dict['length'],
                    year = film_dict['year'],
                    director = film_dict['director'])
        for actor in film_dict['actors']:
            film.actors.append(Actor(actor['name']))
        film.save()
        resp = film_schema.dump(film)
        return resp, 201

class FilmResource(Resource):
    def get(self, id):
        film = Film.get_by_id(id)
        if film is None:
            raise ObjectNotFound('La pelicula no existe')
        resp = film_schema.dump(film)
        return resp

api = Api(films_v1_0_bp)
api.add_resource(FilmListResource, '/api/v1.0/films/', endpoint = 'film_list_resource')
api.add_resource(FilmResource, '/api/v1.0/films/<int:id>', endpoint = 'film_resource')

