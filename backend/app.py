from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import mysql.connector
from db_config import DB_CONFIG


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
  # This will allow cross-origin requests from any origin

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.response_class()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response


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
'''@app.route('/register', methods=['POST'])
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
'''
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

    # Application-level validation
    # Check required fields
    if not all([email_id, password, first_name]):
        return jsonify({'error': 'Email, password, and first name are required!'}), 400

    # Validate budgets
    if not (200 <= accommodation_budget <= 22000):
        return jsonify({'error': 'Accommodation budget must be between 200 and 22000!'}), 400

    if not (0 <= tuition_fee_budget <= 60000):
        return jsonify({'error': 'Tuition fee budget must be between 0 and 60000!'}), 400

    # Ensure selected colleges exist in the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch valid university names
        cursor.execute("SELECT UniversityName FROM University")
        valid_universities = {row[0] for row in cursor.fetchall()}

        # Check if all selected colleges are valid
        invalid_colleges = [college for college in selected_colleges if college not in valid_universities]
        if invalid_colleges:
            return jsonify({'error': f'Invalid universities selected: {invalid_colleges}'}), 400

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

# Route for getting user info 
@app.route('/userInfo/<int:id>', methods=['GET'])
def get_user_info(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user details
        user_query = """
            SELECT FirstName, LastName, EmailId, TuitionFeeBudget, AccommodationBudget
            FROM User
            WHERE Id = %s
        """
        cursor.execute(user_query, (id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found!'}), 404

        # Fetch universities selected by the user
        univ_query = """
            SELECT UniversityName
            FROM User_UnivShortlist
            WHERE UserId = %s
        """
        cursor.execute(univ_query, (id,))
        universities = [row[0] for row in cursor.fetchall()]

        # Construct user info response
        user_info = {
            'FirstName': user[0],
            'LastName': user[1],
            'EmailId': user[2],
            'TuitionFeeBudget': user[3],
            'AccommodationBudget': user[4],
            'SelectedUniversities': universities
        }

        return jsonify(user_info), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/updateUniversity', methods=['POST'])
def update_universities():
    data = request.json
    user_id = data.get('userId')
    old = data.get('oldUniversity')
    new = data.get('updatedUniversity')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the university name in User_UnivShortlist
        update_query = """
            UPDATE User_UnivShortlist
            SET UniversityName = %s
            WHERE UserId = %s AND UniversityName = %s
        """
        cursor.execute(update_query, (new, user_id, old))

        # Check if the update affected any rows
        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching university found for the update.'}), 404

        conn.commit()
        return jsonify({'message': 'University updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/removeUniversity', methods=['POST'])
def delete_universities():
    data = request.json
    user_id = data.get('userId')
    UnivDelete = data.get('university')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete specified universities from User_UnivShortlist
        delete_query = """
            DELETE FROM User_UnivShortlist 
            WHERE UserId = %s AND UniversityName = %s
        """
        cursor.execute(delete_query, (user_id, UnivDelete))

        conn.commit()
        return jsonify({'message': 'Selected universities deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# @app.route('/getUniversityDetails/<int:Id>', methods=['GET'])
# def get_university_details(Id):
#     try:
#         # Connect to the database
#         conn = get_db_connection()
#         cursor = conn.cursor(buffered=True)

#         sp_query = f"CALL GetUniversityDetails({Id});"

#         cursor.execute(sp_query)
#         while cursor.nextset():
#             pass  
#         results = cursor.fetchall()

#         column_names = [desc[0] for desc in cursor.description]
#         universities_details = [dict(zip(column_names, row)) for row in results]
#         while cursor.nextset():
#             pass

#         print(universities_details)
#         return jsonify(universities_details), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()

@app.route('/getUniversityDetails/<int:Id>', methods=['GET'])
def get_university_details(Id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Use callproc instead of execute for stored procedures
        cursor.callproc('GetUniversityDetails', [Id])
        
        # Fetch results from the first result set
        results = next(cursor.stored_results())
        universities_details = results.fetchall()
        print(universities_details)
        return jsonify(universities_details), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/matching-universities/<int:user_id>', methods=['GET'])
def get_matching_universities(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute the stored procedure using raw SQL
        cursor.execute("CALL GetMatchingUniversities(%s)", (user_id,))

        # Fetch all results
        matching_universities = cursor.fetchall()

        return jsonify(matching_universities), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/matching-universities/search/<int:user_id>/<string:key_word>', methods=['GET'])
def search_matching_universities(user_id, key_word):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute the stored procedure to fetch universities matching the user budget and search keyword
        cursor.execute("CALL SearchMatchingUniversities(%s, %s)", (user_id, key_word))

        # Fetch all results
        matching_universities = cursor.fetchall()

        return jsonify(matching_universities), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/getUserLivingCosts/<int:user_id>', methods=['GET'])
def get_user_living_costs(user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Raw SQL query to execute the stored procedure
        query = """
            CALL GetUserLivingCosts(%s)
        """
        cursor.execute(query, (user_id,))

        # Fetch results from the stored procedure
        living_costs = cursor.fetchall()

        return jsonify(living_costs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
