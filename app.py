from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, json
import os
from extraction import extract_aadhaar_details, extract_community_details, extract_income_details

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/women')
def women():
    return render_template('womendoc.html')

@app.route('/womenform')
def form_page():
    return render_template('womenform.html')

@app.route('/schemes')
def schemes():
    # Read schemes from a JSON or text file
    try:
        with open('text/submit.txt', 'r') as f:
            data = f.read()
        return render_template('schemes.html', data=data)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('home'))  # Redirect to home if error occurs

@app.route('/schemepage/<scheme_id>')
def schemepage(scheme_id):
    # Here, you can parse the scheme details based on the scheme_id from the text/JSON
    try:
        with open(f'text/{scheme_id}.json', 'r') as f:
            scheme_data = json.load(f)
        return render_template('schemepage.html', scheme=scheme_data)
    except Exception as e:
        flash(f'Error loading scheme: {str(e)}', 'danger')
        return redirect(url_for('schemes'))  # Redirect to schemes page on error

@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    # (same as your existing code for document upload and extraction)
    pass

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Ensure the text directory exists
        if not os.path.exists('text'):
            os.makedirs('text')

        # Get form data
        age = request.form.get('age')
        state = request.form.get('state')
        community = request.form.get('community')
        income = request.form.get('income')
        marital_status = request.form.get('marital-status')
        area = request.form.get('area')
        differently_abled = request.form.get('differently-abled')
        student = request.form.get('student')

        # Prepare the data to be saved
        data_to_save = {
            "age": age,
            "state": state,
            "community": community,
            "income": income,
            "marital_status": marital_status,
            "area": area,
            "differently_abled": differently_abled,
            "student": student
        }

        # Save to a JSON file
        with open(os.path.join('text', 'submit.json'), 'w') as f:
            json.dump(data_to_save, f)

        flash('Form submitted successfully!', 'success')  # Flash message for success
        return redirect(url_for('schemes'))  # Redirect to schemes page

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')  # Flash message for error
        return redirect(url_for('schemes'))  # Redirect to schemes page

if __name__ == '__main__':
    app.run(debug=True)
