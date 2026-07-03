from flask import Flask, request, jsonify
import pymysql
import os
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'static/images'

# ---------- MYSQL CONNECTION ----------
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='utensils',
        port=3307,
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------- SIGNUP ----------
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    role=request.form['role']

    if not all([name, password, email, phone]):
        return jsonify({'status': 'failed', 'message': 'All fields are required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = %s OR email = %s OR phone = %s", (name, email, phone))
    if cursor.fetchone():
        return jsonify({'status': 'failed', 'message': 'User already exists'}), 409

    cursor.execute("INSERT INTO users (name, password, email, phone, role) VALUES (%s, %s, %s, %s,%s)", (name, password, email, phone,role))
    conn.commit()
    return jsonify({'status': 'success', 'message': 'User registered'}), 201

# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({'status': 'success', 'user': user}), 200
    else:
        return jsonify({'status': 'failed', 'message': 'Invalid credentials'}), 401

# ---------- RESET PASSWORD ----------
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", (password, email))
    conn.commit()
    return jsonify({'status': 'success', 'message': 'Password reset'}), 200

# ---------- UPDATE PROFILE ----------
@app.route('/update_profile', methods=['POST'])
def update_profile():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = %s, phone = %s WHERE name = %s", (email, phone, name))
    conn.commit()
    return jsonify({'status': 'success', 'message': 'Profile updated'}), 200

# ---------- ADD PRODUCT ----------
@app.route('/add_products', methods=['POST'])
def add_products():
    data = request.form
    image = request.files.get('product_photo')
    if not image:
        return jsonify({'status': 'failed', 'message': 'Image required'}), 400

    filename = image.filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(path)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (product_name, product_cost, product_description, product_category, product_photo)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['product_name'], data['product_cost'], data['product_description'], data['product_category'], filename))
    conn.commit()
    return jsonify({'status': 'success', 'message': 'Product added'}), 201

# ---------- GET PRODUCTS ----------
@app.route('/get_products', methods=['GET'])
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    return jsonify(cursor.fetchall()), 200

# ---------- DELETE PRODUCT (admin only) ----------
@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 403

    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    conn.commit()
    return jsonify({'status': 'success', 'message': 'Product deleted'}), 200


# ---------- ADD REVIEW ----------
@app.route('/add_review', methods=['POST'])
def add_review():
    user_id = request.form.get('user_id')
    product_id = request.form.get('product_id')
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (user_id, product_id, rating, comment, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (user_id, product_id, rating, comment))
    conn.commit()
    return jsonify({'status': 'success', 'message': 'Review added'}), 201

# ---------- GET REVIEWS ----------
@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.reviews_id, u.name, p.product_name, r.rating, r.comment, r.created_at
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        JOIN products p ON r.product_id = p.product_id
    """)
    rows = cursor.fetchall()
    for row in rows:
        row['created_at'] = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'reviews': rows}), 200

# ---------- DELETE REVIEW (user or admin) ----------
@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    if not user:
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 403

    cursor.execute("DELETE FROM reviews WHERE reviews_id = %s", (review_id,))
    conn.commit()
    return jsonify({'status': 'success', 'message': 'Review deleted'}), 200

# ---------- ADMIN DASHBOARD ----------
@app.route("/admin-dashboard", methods=["POST"])
def admin_dashboard():
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if not user or user['role'] != 'admin':
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 403

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.execute("""
        SELECT o.order_id, o.quantity, o.order_date, u.name, p.product_name
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        JOIN products p ON o.product_id = p.product_id
    """)
    orders = cursor.fetchall()
    cursor.execute("""
        SELECT r.reviews_id, u.name, p.product_name, r.rating, r.comment, r.created_at
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        JOIN products p ON r.product_id = p.product_id
    """)
    reviews = cursor.fetchall()
    for r in reviews:
        r['created_at'] = r['created_at'].strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({
        "status": "success",
        "products": products,
        "users": users,
        "orders": orders,
        "reviews": reviews
    }), 200





@app.route('/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        # Extract POST Values sent
        amount = request.form['amount']
        phone = request.form['phone']

        # Provide consumer_key and consumer_secret provided by safaricom
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        # Authenticate Yourself using above credentials to Safaricom Services
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        data = response.json()
        access_token = "Bearer " + data['access_token']

        # Getting the password
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data_to_encode = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data_to_encode.encode())
        password = encoded.decode()

        # Payload
        payload = {
            "BusinessShortCode": "174379",
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://coding.co.ke/confirm.php",
            "AccountReference": "SokoGarden Online",
            "TransactionDesc": "Payments for products or product"
        }

        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)

        return jsonify({"message": "An MPESA Prompt has been sent to Your Phone, Please Check & Complete Payment"})

# ---------- RUN FLASK ----------
if __name__ == '__main__':
    app.run(debug=True)

