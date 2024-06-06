import pytest
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from flask_login import login_user, logout_user
from app import create_app, db
from app.characters.models import Character
from app.users.model import User

characters = [
    {
        "literal": "一",
        "ucs": "4e00",
        "jis208": "1-16-76",
        "radical": "⼀",
        "stroke_count": 1,
        "grade": 1,
        "nelson_n": 1,
        "heisig6": 1,
        "halpern_kkd": 4148,
        "halpern_kkld_2ed": 2850,
    }
]

@pytest.fixture(scope="module")
def app():
    return create_app("test")

@pytest.fixture(scope="module")
def client(app):
    with app.app_context():
        yield app.test_client()

@pytest.fixture(autouse=True)
def init_db():
    db.create_all()

    for character in characters:
        character = Character(**character)
        db.session.add(character)
    db.session.commit()

    yield

    db.close_all_sessions()
    db.drop_all()

@pytest.fixture(autouse=True)
def logout(app):
    yield
    with app.test_request_context():
        logout_user()

@pytest.fixture(scope="function")
def default_user(app):
    user = User(username="teemu", email="teemu@email.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    with app.test_request_context():
        login_user(user)
    return user

@pytest.fixture(scope="function")
def fetch(client):
    def _fetch(url, params=None, data=None, flash=False):
        if params:
            url += "?" + urlencode(params)

        if data is not None:
            r = client.post(url, data=data, follow_redirects=True)
        else:
            r = client.get(url, follow_redirects=True)

        soup = BeautifulSoup(r.data, "html.parser")

        if flash:
            msg = [msg.text for msg in soup.select("#flashes .message")]
            err = [error.text for error in soup.select("#flashes .error")]
            return soup, {"msg": msg, "err": err}
        else:
            return soup

    return _fetch