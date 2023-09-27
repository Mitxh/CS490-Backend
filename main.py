from flask import Flask, jsonify, request
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

@app.route('/actors_movies')
def movies_of_actors():
  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  query = 'SELECT film.film_id, film_actor.actor_id AS actor_id, film.title, COUNT(rental.rental_id) AS count FROM film JOIN inventory ON film.film_id = inventory.film_id JOIN rental ON inventory.inventory_id = rental.inventory_id JOIN film_actor ON film.film_id = film_actor.film_id GROUP BY film.film_id, film_actor.actor_id ORDER BY film_actor.actor_id ASC, count DESC;'
  cursor.execute(query)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()
  results = [list(row) for row in results]
  for i in range(len(results)):
    results[i][2] = results[i][2].title()
  return jsonify(results)

@app.route('/customer_search')
def customer_search():
  search_term = request.args.get('search_term', '')
  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  if search_term:
    query = f"SELECT customer_id, first_name, last_name FROM customer WHERE first_name LIKE '%{search_term}%' OR last_name LIKE '%{search_term}%' OR customer_id LIKE '%{search_term}%';"
  else:
    query = 'SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer WHERE customer.active=1;'
  cursor.execute(query)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()
  results = [list(row) for row in results]
  for i in range(len(results)):
    results[i][1] = results[i][1].title()
    results[i][2] = results[i][2].title()
  return jsonify(results)

@app.route('/add_customer', methods=['POST'])
def add_customer():
  customer = request.json
  first_name = customer['first_name']
  last_name = customer['last_name']
  email = customer['email']
  address_1 = customer['address_1']
  address_2 = customer['address_2']
  district = customer['district']
  postal_code = customer['postal_code']
  phone = customer['phone']

  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()

  query = "SELECT customer_id FROM customer ORDER BY customer_id DESC LIMIT 1;"
  cursor.execute(query)
  lastCustomerID = cursor.fetchall()[0][0]
  query = "SELECT city_id FROM city ORDER BY city_id DESC LIMIT 1;"
  cursor.execute(query)
  lastCityID = cursor.fetchall()[0][0]
  query = "SELECT address_id FROM address ORDER BY address_id DESC LIMIT 1;" 
  cursor.execute(query)
  lastAddressID = cursor.fetchall()[0][0]

  query = f"INSERT INTO city VALUES ('{lastCityID+1}', '{district}', 103, NOW());"
  cursor.execute(query)
  query = f"INSERT INTO address VALUES ('{lastAddressID+1}', '{address_1}', '{address_2}', '{district}', '{lastCityID+1}', '{postal_code}', '{phone}', ST_GeomFromText('POINT(128.0449753 46.9804391)'), NOW());"
  cursor.execute(query)
  query = f"INSERT INTO customer VALUES ('{lastCustomerID+1}', 2, '{first_name}', '{last_name}', '{email}', '{lastAddressID+1}', 1, NOW(), NOW());"
  cursor.execute(query)
  
  cnx.commit()
  cursor.close()
  cnx.close()
  
  return jsonify({
    'status': "User Added",
    'customer':{
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'address_1': address_1,
      'address_2': address_2,
      'district': district,
      'postal_code': postal_code,
      'phone': phone,
      'customer_id': lastCustomerID,
      'city_id': lastCityID,
      'address_id': lastAddressID
    }
  })

if __name__ == "__main__":
  app.run(debug=True)
