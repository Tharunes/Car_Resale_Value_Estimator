from flask import Flask, render_template, request, jsonify, redirect, url_for, session

# Additional imports for the example
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__, template_folder='Templates')

# Replace 'dummy_secret_key' with a secure secret key
app.secret_key = 'eba97863988ae8e349277072f18b45fb'

model = pickle.load(open('rf_regression_model.pkl', 'rb'))

standard_to = StandardScaler()

@app.route('/', methods=['GET'])
def Home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route("/predict", methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        Year = 2020 - Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = request.form['Transmission_Mannual']
        if Transmission_Mannual == 'Mannual':
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                    Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car !")
        else:
            return render_template('index.html', prediction_text=" {} ".format(output))
    else:
        return render_template('index.html')

# New route for the company details page
@app.route('/company_details')
def company_details():
    return render_template('company_details.html')

@app.route("/calculate_loan", methods=['GET'])
def calculate_loan():
    # Placeholder loan amounts for demonstration purposes
    loan_6_months = round(np.random.uniform(40000, 50000), 2)
    loan_10_months = round(np.random.uniform(30000, 35000), 2)
    loan_12_months = round(np.random.uniform(28000, 12000), 2)

    # Return the loan amounts as JSON
    return jsonify({
        'loan_6_months': loan_6_months,
        'loan_10_months': loan_10_months,
        'loan_12_months': loan_12_months
    })

# New login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check user credentials (replace this with your authentication logic)
        username = request.form['username']
        password = request.form['password']

        # Replace this with your actual authentication logic
        # For example, check if the username and password match a stored user
        if username == 'your_username' and password == 'your_password':
            session['logged_in'] = True
            return redirect(url_for('Home'))

        # If authentication fails, redirect back to the login page
        return render_template('login.html', error='Invalid username or password')

    # If the request is a GET, render the login form
    return render_template('login.html')

# New logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
