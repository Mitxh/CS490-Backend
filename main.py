from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
# from healthcheck import HealthCheck
app = Flask(__name__)
CORS(app)

@app.route('/movies')
def movie_list():
  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  query = 'SELECT film.film_id, film.title AS title, COUNT(*) AS count, film.description FROM rental INNER JOIN inventory ON inventory.inventory_id=rental.inventory_id INNER JOIN film ON inventory.film_id=film.film_id GROUP BY film_id, title ORDER BY count DESC LIMIT 5;'
  cursor.execute(query)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()
  results = [list(row) for row in results]
  for i in range(len(results)):
    results[i][1] = results[i][1].title()
  return jsonify(results)

@app.route('/actors')
def actor_list():
  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  query = 'SELECT actor.actor_id, actor.first_name AS "First", actor.last_name AS "Last", COUNT(film_id) AS "Film Count" FROM actor INNER JOIN film_actor ON film_actor.actor_id=actor.actor_id GROUP BY actor.actor_id ORDER BY COUNT(film_id) DESC LIMIT 5;'
  cursor.execute(query)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()
  results = [list(row) for row in results]
  for i in range(len(results)):
    results[i][1] = results[i][1].title()
    results[i][2] = results[i][2].title()
  return jsonify(results)

if __name__ == "__main__":
  app.run(debug=True)
  #test
