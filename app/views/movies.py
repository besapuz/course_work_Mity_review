from flask import request, jsonify
from flask_restx import Namespace, Resource
from app.container import movie_service
from app.dao.models.movie import MovieSchema
from app.decorators import auth_required, admin_required

movies_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@movies_ns.route('/')
class MovieView(Resource):
    # @auth_required
    def get(self):
        page = request.args.get('pages')
        status=request.args.get('status')
        if page:
            movies = movie_service.get_by_page(int(page))
        elif status == 'new':
            movies = movie_service.get_newest()
        else:
            movies = movie_service.get_all()
        return movies_schema.dump(movies), 200

    @admin_required
    def post(self):
        data = request.get_json()
        movie_service.create(data)
        movie_id = data['id']
        response = jsonify()
        response.status_code = 201
        response.headers['location'] = f'/{movie_id}'
        return response


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)

        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid):
        data = request.get_json()
        data['id'] = mid
        movie_service.update(data)

        return '', 204

    @admin_required
    def patch(self, mid):
        data = request.get_json()
        data['id'] = mid
        movie_service.update(data)
        return '', 204

    @admin_required
    def delete(self, mid):
        movie_service.delete(mid)

        return '', 204
