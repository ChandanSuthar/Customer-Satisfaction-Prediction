from flask import Flask, render_template, url_for, request
import mysql.connector as mc
import joblib

app = Flask(__name__)

model = joblib.load('logistic_regression.lb')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'userdb'
}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/project_form')
def project_form():
    return render_template('project.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        age = int(request.form['age'])
        flight_distance = int(request.form['flight_distance'])
        inflight_entertainment = int(request.form['inflight-entertainment'])
        baggage_handling = int(request.form['baggage-handling'])
        cleanliness = int(request.form['cleanliness'])
        departure_delay = int(request.form['departure_delay'])
        arrival_delay = int(request.form['arrival_delay'])
        gender = int(request.form['gender'])
        customer_type = int(request.form['customer-type'])
        travel_type = int(request.form['travel-type'])
        class_type = request.form['class-type']
        Class_Eco = 0
        Class_Eco_Plus = 0
        if class_type == 'ECO':
            Class_Eco = 1
            Class_Eco_Plus = 0
        elif class_type == 'ECO_PLUS':
            Class_Eco = 0
            Class_Eco_Plus = 1
        else:
            Class_Eco = 0
            Class_Eco_Plus = 0

        # Prepare data for the prediction model
        UNSEEN_DATA = [[age, flight_distance, inflight_entertainment, baggage_handling, cleanliness, departure_delay, arrival_delay, gender, customer_type, travel_type, Class_Eco, Class_Eco_Plus]]

        # Make the prediction
        prediction = model.predict(UNSEEN_DATA)[0]
        labels = {'1': "SATISFIED", '0': "DISATISFIED"}
        output = labels[str(prediction)]

        # Save the input data and prediction output to the database
        conn = mc.connect(**db_config)
        cur = conn.cursor()

        insert_query = """
        INSERT INTO customer_satisfaction (age, flight_distance, inflight_entertainment, baggage_handling, cleanliness, departure_delay, arrival_delay, gender, customer_type, travel_type, Class_Eco, Class_Eco_Plus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (age, flight_distance, inflight_entertainment, baggage_handling, cleanliness, departure_delay, arrival_delay, gender, customer_type, travel_type, Class_Eco, Class_Eco_Plus))
        
        # Save the prediction output
        insert_prediction_query = """
        INSERT INTO Prediction (output)
        VALUES (%s)
        """
        cur.execute(insert_prediction_query, (output,))
        
        conn.commit()
        cur.close()
        conn.close()

        # Return the prediction result
        return render_template('output.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
