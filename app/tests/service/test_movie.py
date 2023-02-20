# import required libraries and modules
from unittest.mock import MagicMock
import pytest
from app.dao.model.movie import Movie
from app.dao.movie import MovieDAO
from app.service.movie import MovieService


# creating fixture to replace logic of data exchange with db
@pytest.fixture()
def movie_dao():
    # creating object of DAO class, with no session that expected to be, as data exchange with db is fake
    movie_dao = MovieDAO(None)

    # creating objects according UML to fill in virtual db
    movie_1 = Movie(id=1, title='film1', description='some text about movie...', trailer='some_link1.com', year=2013,
                    rating=8.5, genre_id=2, director_id=1)
    movie_2 = Movie(id=2, title='film2', description='some another text about movie...', trailer='some_link2.com',
                    year=2013,
                    rating=8.6, genre_id=1, director_id=2)
    movie_3 = Movie(id=3, title='film3', description='some other text about movie...', trailer='some_link3.com',
                    year=2013,
                    rating=8.7, genre_id=3, director_id=3)

    # replace result of relative methods with data in expected formats or types
    movie_dao.get_one = MagicMock(return_value=movie_3)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=4, title='film4', description='some more text about movie...',
                                                    trailer='some_link4.com', year=2013, rating=8.5, genre_id=2,
                                                    director_id=1))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


# creating class for business logics testing - methods execution
class TestMovieService:
    # creating fixture to execute during test, auto use true executes fixture before all further tests
    @pytest.fixture(autouse=True)
    # fixture adds attribute movie_service to class TestMovieService. Attribute is creating as object of
    # MovieService class using movie_dao, which came from fixture above
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(movie_dao)

    def test_get_one(self):
        """
        applying tested method to movie_service, checking if data from mocked dao appears
        """
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None
        assert movie.title is not None
        assert movie.description is not None
        assert movie.trailer is not None
        assert movie.year is not None
        assert movie.rating is not None
        assert movie.genre_id is not None
        assert movie.director_id is not None

    def test_get_all(self):
        """
        applying tested method to movie_service, checking if data from mocked dao appears
        """
        movies = self.movie_service.get_all()

        assert movies is not None
        assert len(movies) > 0
        for movie in movies:
            assert movie is not None
            assert movie.title is not None
            assert movie.description is not None
            assert movie.trailer is not None
            assert movie.year is not None
            assert movie.rating is not None
            assert movie.genre_id is not None
            assert movie.director_id is not None

    def test_create(self):
        """
        applying tested method to movie_service, checking if data from mocked dao appears
        """
        movie_data = {
            'id': 4,
            'title': 'film4',
            'description': 'some more text about movie...',
            'trailer': 'some_link4.com',
            'year': 2013,
            'rating': 8.5,
            'genre_id': 2,
            'director_id': 1
        }

        movie = self.movie_service.create(movie_data)
        assert movie.id is not None
        assert movie.title is not None
        assert movie.description is not None
        assert movie.trailer is not None
        assert movie.year is not None
        assert movie.rating is not None
        assert movie.genre_id is not None
        assert movie.director_id is not None

    def test_delete(self):
        """
        applying tested method to movie_service, no assert as method returns nothing
        """
        self.movie_service.delete(1)

    def test_update(self):
        """
        applying tested method to movie_service, no assert as method returns nothing
        """
        movie_data = {
            "id": 4,
            "title": "new name"
        }
        self.movie_service.update(movie_data)
