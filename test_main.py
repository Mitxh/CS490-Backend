import pytest
from main import app
import json

@pytest.fixture
def client():
  app.config['TESTING'] = True
  with app.test_client() as client:
    yield client
# actor tests
def test_actorList(client):
  actorListRes = client.get('/actors')
  assert actorListRes.status_code == 200
  data = json.loads(actorListRes.data)
  # GENERALS
  assert len(data) == 5
  for i in range(5):
    assert len(data[i]) == 4
    if (i < 3):
      assert data[i][3] >= data[i+1][3]
  # SPECIFICS
  assert data[0][0] == 107
  assert data[1][0] == 102
  assert data[2][0] == 198
  assert data[3][0] == 181
  assert data[4][0] == 23

# actors movies
def test_actorsMovies(client):
  actorsMoviesRes = client.get('/actors_movies')
  assert actorsMoviesRes.status_code == 200
  data = json.loads(actorsMoviesRes.data)
  lastI = 0
  # GENERALS
  for i in range(len(data)):
    # checking if actor_id is in correct order
    if(i != len(data)-1):
      assert data[i][1] <= data[i+1][1]
      if(lastI == i):
        assert data[i][3] >= data[i+1][3]
    lastI = i
  # SPECIFICS
  assert data[0][2] == "Gleaming Jawbreaker"
  assert data[1][2] == "Westward Seabiscuit"
  assert data[2][2] == "Color Philadelphia"
  assert data[3][2] == "Academy Dinosaur"
  assert data[4][2] == "Angels Life"
  assert data[5][2] == "Anaconda Confessions"
  assert data[6][2] == "Cheaper Clyde"
  assert data[7][2] == "Lady Stage"
  assert data[8][2] == "Rules Human"
  assert data[9][2] == "Wizard Coldblooded"
  assert data[10][2] == "Human Graffiti"
  assert data[11][2] == "Elephant Trojan"
  assert data[12][2] == "Splash Gump"
  assert data[13][2] == "Language Cowboy"
  assert data[14][2] == "King Evolution"
  assert data[15][2] == "Vertigo Northwest"
  assert data[16][2] == "Bulworth Commandments"
  assert data[17][2] == "Mulholland Beast"
  assert data[18][2] == "Oklahoma Jumanji"

# movie list
def test_movies(client):
  movieListRes = client.get('/movies')
  assert movieListRes.status_code == 200
  data = json.loads(movieListRes.data)
  # GENERALS
  assert len(data) == 5
  for i in range(5):
    assert len(data[i]) == 4
    if (i < 3):
      assert data[i][2] >= data[i+1][2]
  # SPECIFICS
  assert data[0][0] == 103
  assert data[1][0] == 738
  assert data[2][0] == 730
  assert data[3][0] == 489
  assert data[4][0] == 767

  assert data[0][1] == "Bucket Brotherhood"
  assert data[1][1] == "Rocketeer Mother"
  assert data[2][1] == "Ridgemont Submarine"
  assert data[3][1] == "Juggler Hardly"
  assert data[4][1] == "Scalawag Duck"