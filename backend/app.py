from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import mysql.connector
from db_config import DB_CONFIG


app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests from any origin

# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG['MYSQL_HOST'],
        user=DB_CONFIG['MYSQL_USER'],
        password=DB_CONFIG['MYSQL_PASSWORD'],
        database=DB_CONFIG['MYSQL_DATABASE']
    )
# Route to fetch university names
@app.route('/universities', methods=['GET'])
def get_university_names():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT UniversityName FROM University"
        cursor.execute(query)
        universities = cursor.fetchall()

        # Extract university names from the result
        university_names = [univ[0] for univ in universities]

        return jsonify(university_names), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# Route for User Registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    first_name = data.get('FirstName')
    last_name = data.get('LastName')
    email_id = data.get('EmailId')
    password = data.get('Password')
    tuition_fee_budget = data.get('TuitionFeeBudget', 0)
    accommodation_budget = data.get('AccommodationBudget', 0)
    selected_colleges = data.get('SelectedColleges', [])

    # Check required fields
    if not all([email_id, password, first_name]):
        return jsonify({'error': 'Email, password, and first name are required!'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM User WHERE EmailId = %s", (email_id,))
        if cursor.fetchone():
            return jsonify({'error': 'User already exists!'}), 409

        # Insert new user into the User table
        user_query = """
            INSERT INTO User (FirstName, LastName, EmailId, Password, TuitionFeeBudget, AccommodationBudget)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(user_query, (first_name, last_name, email_id, password, tuition_fee_budget, accommodation_budget))
        user_id = cursor.lastrowid

        # Insert selected universities into User_UnivShortlist table
        univ_query = "INSERT INTO User_UnivShortlist (UserId, UniversityName) VALUES (%s, %s)"
        for college in selected_colleges:
            cursor.execute(univ_query, (user_id, college))

        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# Route for User Login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email_id = data.get('EmailId')
    password = data.get('Password')

    if not all([email_id, password]):
        return jsonify({'error': 'Email and password are required!'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check user credentials (without hashing)
        query = "SELECT Id, FirstName, LastName, EmailId, Password FROM User WHERE EmailId = %s AND Password = %s"
        cursor.execute(query, (email_id, password))
        user = cursor.fetchone()

        if user:
            return jsonify({'message': 'Login successful!', 'user': user}), 200
        else:
            return jsonify({'error': 'Invalid email or password!'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
