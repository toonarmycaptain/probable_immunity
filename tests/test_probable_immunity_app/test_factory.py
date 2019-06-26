from probable_immunity_app import about_text_string, create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_about_text(client):
    response = client.get('/about_text')
    assert response.data == about_text_string