# import required libraries and modules
from unittest.mock import MagicMock
import pytest
from app.dao.model.genre import Genre
from app.dao.genre import GenreDAO
from app.service.genre import GenreService


# creating fixture to replace logic of data exchange with db
@pytest.fixture()
def genre_dao():
    # creating object of DAO class, with no session that expected to be, as data exchange with db is fake
    genre_dao = GenreDAO(None)

    # creating objects according UML to fill in virtual db
    genre_1 = Genre(id=1, name='comedy')
    genre_2 = Genre(id=2, name='drama')
    genre_3 = Genre(id=3, name='porn')

    # replace result of relative methods with data in expected formats or types
    genre_dao.get_one = MagicMock(return_value=genre_3)
    genre_dao.get_all = MagicMock(return_value=[genre_1, genre_2, genre_3])
    genre_dao.create = MagicMock(return_value=Genre(id=4, name='horror'))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


# creating class for business logics testing - methods execution
class TestGenreService:
    # creating fixture to execute during test, auto use true executes fixture before all further tests
    @pytest.fixture(autouse=True)
    # fixture adds attribute genre_service to class TestGenreService. Attribute is creating as object of
    # GenreService class using genre_dao, which came from fixture above
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(genre_dao)

    def test_get_one(self):
        """
        applying tested method to genre_service, checking if data from mocked dao appears
        """
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id is not None
        assert genre.name is not None

    def test_get_all(self):
        """
        applying tested method to genre_service, checking if data from mocked dao appears
        """
        genres = self.genre_service.get_all()

        assert genres is not None
        assert len(genres) > 0
        for genre in genres:
            assert genre is not None
            assert genre.id is not None
            assert genre.name is not None

    def test_create(self):
        """
        applying tested method to genre_service, checking if data from mocked dao appears
        """
        genre_data = {
            "name": "biopic"
        }

        genre = self.genre_service.create(genre_data)
        assert genre.id is not None
        assert genre.name is not None

    def test_delete(self):
        """
        applying tested method to genre_service, no assert as method returns nothing
        """
        self.genre_service.delete(1)

    def test_update(self):
        """
        applying tested method to genre_service, no assert as method returns nothing
        """
        genre_data = {
            "id": 3,
            "name": "biopic"
        }
        self.genre_service.update(genre_data)
