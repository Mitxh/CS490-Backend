from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
# from healthcheck import HealthCheck
app = Flask(__name__)
CORS(app)
# health=HealthCheck()
# def test():
#    return True, "Hello World"
# health.add_check(test)
# app.add_url_rule('/healthcheck', 'healthcheck', view_func=lamda: health.run())
cnx = mysql.connector.connect(
    user='root', password='Mb235957', host='localhost', database='sakila')


@app.route('/')
def heath_check():
    #  return jsonify(status=200, print="Hello World")
    cursor = cnx.cursor()
    query = 'SELECT film.film_id, film.title AS title, COUNT(*) AS count FROM rental INNER JOIN inventory ON inventory.inventory_id=rental.inventory_id INNER JOIN film ON inventory.film_id=film.film_id GROUP BY film_id, title ORDER BY count DESC LIMIT 5;'
    cursor.execute(query)
    results = cursor.fetchall()

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
