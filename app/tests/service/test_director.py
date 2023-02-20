# import required libraries and modules
from unittest.mock import MagicMock
import pytest
from app.dao.model.director import Director
from app.dao.director import DirectorDAO
from app.service.director import DirectorService


# creating fixture to replace logic of data exchange with db
@pytest.fixture()
def director_dao():
    # creating object of DAO class, with no session that expected to be, as data exchange with db is fake
    director_dao = DirectorDAO(None)

    # creating objects according UML to fill in virtual db
    director_1 = Director(id=1, name='John Doe')
    director_2 = Director(id=2, name='Jane Doe')
    director_3 = Director(id=3, name='Jan Itor')

    # replace result of relative methods with data in expected formats or types
    director_dao.get_one = MagicMock(return_value=director_3)
    director_dao.get_all = MagicMock(return_value=[director_1, director_2, director_3])
    director_dao.create = MagicMock(return_value=Director(id=4, name='Head Dick'))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


# creating class for business logics testing - methods execution
class TestDirectorService:
    # creating fixture to execute during test, auto use true executes fixture before all further tests
    @pytest.fixture(autouse=True)
    # fixture adds attribute director_service to class TestDirectorService. Attribute is creating as object of
    # DirectorService class using director_dao, which came from fixture above
    def director_service(self, director_dao):
        self.director_service = DirectorService(director_dao)

    def test_get_one(self):
        """
        applying tested method to director_service, checking if data from mocked dao appears
        """
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None
        assert director.name is not None

    def test_get_all(self):
        """
        applying tested method to director_service, checking if data from mocked dao appears
        """
        directors = self.director_service.get_all()

        assert directors is not None
        assert len(directors) > 0
        for director in directors:
            assert director is not None
            assert director.id is not None
            assert director.name is not None

    def test_create(self):
        """
        applying tested method to director_service, checking if data from mocked dao appears
        """
        director_data = {
            "name": "dir dir"
        }

        director = self.director_service.create(director_data)
        assert director.id is not None
        assert director.name is not None

    def test_delete(self):
        """
        applying tested method to director_service, no assert as method returns nothing
        """
        self.director_service.delete(1)

    def test_update(self):
        """
        applying tested method to director_service, no assert as method returns nothing
        """
        director_data = {
            "id": 2,
            "name": "dir dir"
        }
        self.director_service.update(director_data)
