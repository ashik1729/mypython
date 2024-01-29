from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import mysql.connector
import json

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mysql",
    "database": "mypython",
}

# Configure the upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    # # Load data from JSON file and insert it into the database
    # with open("items.json", "r") as json_file:
    #     data = json.load(json_file)
    #     connection = mysql.connector.connect(**db_config)
    #     cursor = connection.cursor()

    #     # Insert data into MySQL database
    #     insert_query = """
    #     INSERT INTO products (
    #         title, description, price, discountPercentage, rating, stock, brand, category, thumbnail, images
    #     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #     """

    #     for product in data["products"]:
    #         values = (
    #             product["title"],
    #             product["description"],
    #             product["price"],
    #             product["discountPercentage"],
    #             product["rating"],
    #             product["stock"],
    #             product["brand"],
    #             product["category"],
    #             product["thumbnail"],
    #             json.dumps(product["images"]),
    #         )
    #         cursor.execute(insert_query, values)

    #     # Commit changes and close connections
    #     connection.commit()
    #     cursor.close()
    #     connection.close()

    return render_template("index.html")


@app.route("/items")
def items():
    # Fetch product data from the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT title, description, thumbnail, price FROM products"

    cursor.execute(query)
    products = cursor.fetchall()

    # print("Fetched products:", products)  # This line prints the products for debugging

    cursor.close()
    connection.close()

    return render_template("items.html", products=products)


# ...


@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    password = request.form["password"]

    # Save file
    file = request.files["file"]
    if file:
        filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filename)
    else:
        filename = None

    # Save data to MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "INSERT INTO user_data (name, email, phone, password, filename) VALUES (%s, %s, %s, %s, %s)"
    values = (name, email, phone, password, filename)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


# API endpoint to get items data
@app.route("/api/items")
def api_items():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM products"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    products = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return jsonify(products)


if __name__ == "__main__":
    app.run(debug=True)
