def test_app_home(app):
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert "Pipesun Backend version" in response.data.decode()
    assert "text/html" in response.content_type


def test_app_docs(app):
    client = app.test_client()

    response = client.get("/swagger-docs")
    assert response.status_code == 200
    assert "text/html" in response.content_type
