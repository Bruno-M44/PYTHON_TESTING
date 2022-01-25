from tkinter.tix import Form
from unicodedata import name

from flask import request
from itsdangerous import json
from server import app, loadClubs, loadCompetitions
import codecs
import pytest

listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()

@pytest.fixture
def client():
  client = app.test_client()
  return client

@pytest.mark.usefixtures("client")
class TestClient:
  def test_home_page(self, client):
    response = client.get('/')
    data = response.data.decode()
    index_content = codecs.open("templates/index.html", 'r').read()
    assert response.status_code == 200
    assert data == index_content

  def test_home_page_with_wrong_email(self, client):
    email="test@test.com"
    response = client.post('/showSummary', data={'email' : email})
    assert response.status_code == 500

  def test_home_page_with_right_email(self, client):
    email="john@simplylift.co"
    response = client.post('/showSummary', data={'email' : email})
    data = response.data.decode("utf-8").replace("%20", " ")
    
    assert response.status_code == 200

    assert data.find("<h2>Welcome, " + email + " </h2>") != -1

    assert data.find("""<a href="/logout">Logout</a>""") != -1

    assert data.find("Points available: " + [club["points"] for club in 
      listOfClubs if club["email"] == email][0]) != -1

    for competition in listOfCompetitions:
      assert data.find(competition["name"]) != -1
      assert data.find("Date: " + competition["date"]) != -1
      assert data.find("Number of Places: " + competition["numberOfPlaces"]) != -1
      assert data.find("""<a href="/book/""" + competition["name"] + 
        """/Simply Lift">Book Places</a>""") != -1

  def test_book_page_display(self, client):
    response = client.get("/book/" + listOfCompetitions[0]["name"] + 
      "/Simply Lift")
    data = response.data.decode()
    assert response.status_code == 200

    assert data.find(listOfCompetitions[0]["name"]) != -1
    assert data.find("Places available: " + 
      listOfCompetitions[0]["numberOfPlaces"]) != -1
  
  def test_book_page_out_of_bounds(self, client):
    places = 68
    response = client.post("/book/" + listOfCompetitions[0]["name"] + 
      "/Simply Lift", data={"places": places})
    assert response.status_code == 200
  
  def test_book_page_within_bounds(self, client):
    places = 12
    print("CLIENT", client)
    response = client.post("/purchasePlaces", 
                            data={ "places" : places })
    assert response.status_code == 200
    
    


