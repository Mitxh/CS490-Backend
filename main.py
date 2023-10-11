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
    query = f"SELECT customer_id, first_name, last_name FROM customer WHERE active=1 AND (first_name LIKE '%{search_term}%' OR last_name LIKE '%{search_term}%' OR customer_id LIKE '%{search_term}%');"
  else:
    query = 'SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer WHERE customer.active=1 ORDER BY customer.last_name;'
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
  city = customer['city']
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

  query = f"INSERT INTO city VALUES ('{lastCityID+1}', '{city}', 103, NOW());"
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
      'city': city,
      'district': district,
      'postal_code': postal_code,
      'phone': phone,
      'customer_id': lastCustomerID,
      'city_id': lastCityID,
      'address_id': lastAddressID
    }
  })

@app.route('/edit_find_customer')
def edit_find_customer():
  customer_id = request.args.get('customerID', '')
  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  query = f"SELECT customer.customer_id, customer.first_name, customer.last_name, customer.email, address.address, address.address2, city.city, address.district, address.postal_code, address.phone FROM customer JOIN address ON address.address_id=customer.address_id JOIN city ON city.city_id=address.city_id WHERE customer_id={customer_id};"
  cursor.execute(query)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()

  first_name = results[0][1]
  last_name = results[0][2]
  email = results[0][3]
  address_1 = results[0][4]
  address_2 = results[0][5]
  city = results[0][6]
  district = results[0][7]
  postal_code = results[0][8]
  phone = results[0][9]
  customer_id = results[0][0]

  return jsonify({
    'status': "User Found",
    'customer':{
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'address_1': address_1,
      'address_2': address_2,
      'city': city,
      'district': district,
      'postal_code': postal_code,
      'phone': phone,
      'customer_id': customer_id
    }
  })

@app.route('/edit_customer', methods=['POST'])
def edit_customer():
  customer = request.json
  first_name = customer['first_name']
  last_name = customer['last_name']
  email = customer['email']
  address_1 = customer['address_1']
  address_2 = customer['address_2']
  city = customer['city']
  district = customer['district']
  postal_code = customer['postal_code']
  phone = customer['phone']
  customer_id = customer['customer_id']
  returnString = ""

  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  query = f"SELECT customer.customer_id, customer.first_name, customer.last_name, customer.email, address.address, address.address2, city.city, address.district, address.postal_code, address.phone FROM customer JOIN address ON address.address_id=customer.address_id JOIN city ON city.city_id=address.city_id WHERE customer_id={customer_id};"
  cursor.execute(query)
  results = cursor.fetchall()

  if(first_name != results[0][1]):
    query = f"UPDATE customer SET first_name='{first_name}' WHERE customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString += "First Name"
  if(last_name != results[0][2]):
    query = f"UPDATE customer SET last_name='{last_name}' WHERE customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "Last Name"
  if(email != results[0][3]):
    query = f"UPDATE customer SET email='{email}' WHERE customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "Email"
  if(address_1 != results[0][4]):
    query = f"UPDATE address JOIN customer ON address.address_id=customer.address_id SET address='{address_1}' WHERE customer.customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "Address1"
  if(address_2 != results[0][5]):
    query = f"UPDATE address JOIN customer ON address.address_id=customer.address_id SET address2='{address_2}' WHERE customer.customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "Address2"
  if(city != results[0][6]):
    query = "SELECT city_id FROM city ORDER BY city_id DESC LIMIT 1;"
    cursor.execute(query)
    lastCityID = cursor.fetchall()[0][0]
    query = f"INSERT INTO city VALUES ('{lastCityID+1}', '{city}', 103, NOW());"
    cursor.execute(query)
    query = f"UPDATE address JOIN customer ON address.address_id=customer.address_id SET city_id='{lastCityID+1}' WHERE customer.customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "City"
  if(district != results[0][7]):
    query = f"UPDATE address JOIN customer ON address.address_id=customer.address_id SET district='{district}' WHERE customer.customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "District"
  if(postal_code != results[0][8]):
    query = f"UPDATE address JOIN customer ON address.address_id=customer.address_id SET postal_code='{postal_code}' WHERE customer.customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "Postal Code"
  if(str(phone) != results[0][9]):
    query = f"UPDATE address JOIN customer ON address.address_id=customer.address_id SET phone='{phone}' WHERE customer.customer_id={customer_id};"
    cursor.execute(query)
    returnString = "" if returnString == "" else returnString + ", "
    returnString = returnString + "Phone"
  returnString = "There were no changes" if returnString == "" else returnString + " were changed"
  cnx.commit()
  cursor.close()
  cnx.close()

  return jsonify({
    'status': returnString,
    'customer':{
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'address_1': address_1,
      'address_2': address_2,
      'city': city,
      'district': district,
      'postal_code': postal_code,
      'phone': phone,
      'customer_id': customer_id
    }
  })
  # return jsonify(customer)

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
  customer = request.json
  customer_id = customer['customer_id']

  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  query = f"SELECT customer_id FROM customer WHERE customer_id={customer_id} and active=1;"
  cursor.execute(query)
  results = cursor.fetchall()
  if(len(results) == 0):
    return jsonify("Customer Not Found")
  query = f"UPDATE customer SET active=0 WHERE customer_id={customer_id};"
  cursor.execute(query)
  cnx.commit()
  cursor.close()
  cnx.close()

  return jsonify("Customer Deleted")

@app.route('/customer_rented')
def customer_rented():
  customer_id = request.args.get('customer_id', '')
  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  query = f"SELECT film.title, film.film_id FROM film JOIN inventory ON inventory.film_id = film.film_id JOIN rental ON rental.inventory_id = inventory.inventory_id JOIN customer ON customer.customer_id = rental.customer_id WHERE customer.customer_id = '{customer_id}';"
  cursor.execute(query)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()
  return(jsonify(results))

@app.route('/movie_search')
def movie_search():
  search_movie = request.args.get('search_movie', '')
  cnx = mysql.connector.connect(user='root', password='Mb235957', host='localhost', database='sakila')
  cursor = cnx.cursor()
  if search_movie:
    query = f"SELECT film.film_id, film.title, film.description, film.release_year, film.rental_rate, film.length, film.rating, film.replacement_cost FROM film JOIN film_actor ON film.film_id = film_actor.film_id JOIN actor ON actor.actor_id = film_actor.actor_id JOIN film_category ON film_category.film_id = film.film_id JOIN category ON category.category_id = film_category.category_id WHERE film.title LIKE '%{search_movie}%' OR actor.first_name LIKE '%{search_movie}%' OR actor.last_name LIKE '%{search_movie}%' OR category.name LIKE '%{search_movie}%';"
  else:
    query = "SELECT film.film_id, film.title, film.description, film.release_year, film.rental_rate, film.length, film.rating, film.replacement_cost FROM film JOIN film_actor ON film.film_id = film_actor.film_id JOIN actor ON actor.actor_id = film_actor.actor_id JOIN film_category ON film_category.film_id = film.film_id JOIN category ON category.category_id = film_category.category_id;"
  cursor.execute(query)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()
  resultsLen = len(results)
  i = 0
  while(i < resultsLen):
    if(i == resultsLen-1):
      print("break")
      break;
    if(results[i][0] == results[i+1][0]):
      print("pop" + str(i+1))
      results.pop(i+1)
      resultsLen -= 1
    else:
      i += 1
  return jsonify(results)

if __name__ == "__main__":
  app.run(debug=True)