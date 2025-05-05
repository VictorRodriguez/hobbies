from flask import Flask, request, redirect, url_for, render_template, jsonify
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'json'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Process the JSON file
        with open(filepath, 'r') as f:
            data = json.load(f)
        # Here you can call your processing function
        processed_data = process_json(data)
        return render_template('result.html', data=processed_data)
    return redirect(request.url)

@app.route('/dashboard')
def dashboard():
    # Read the JSON file
    with open('/var/www/html/summary.json', 'r') as f:
        summary_data = json.load(f)

    # Define the base URL for the files
    base_url = "http://10.88.81.169:8081"  # Replace with your actual base URL

    # Render the dashboard template with the summary data and base URL
    return render_template('dashboard.html', summary=summary_data, base_url=base_url)

def process_json(data):
    # Implement your JSON processing logic here
    # For example, let's just return the data as-is
    return data


if __name__ == '__main__':
    app.run(debug=True)

