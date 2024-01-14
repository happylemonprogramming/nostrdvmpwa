from flask import Flask, render_template, send_file
import subprocess
import os

app = Flask(__name__, template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html',STREAMLIT_URL=os.environ.get('STREAMLIT_URL'))

# @app.route('/streamlit')
# def streamlit():
#     st.set_page_config(page_title="My Streamlit App")
#     st.write("Hello, world!")

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

# streamlit_process = subprocess.Popen(['streamlit', 'run', 'Home.py'])

if __name__ == '__main__':
    # # Start Streamlit in a separate process
    # streamlit_process = subprocess.Popen(['streamlit', 'run', 'Home.py'])

    # Run Flask app with Gunicorn
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    # # Ensure Streamlit process terminates when Flask app stops
    # streamlit_process.terminate()
