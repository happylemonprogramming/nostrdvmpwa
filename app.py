from flask import Flask, render_template, send_file, request, jsonify, session
from lightninglogin import generate_auth_url
from database import *
import qrcode
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html', streamlit_url=os.environ.get('streamlit_url'))

@app.route('/lightninglogin')
def login():
    # Example usage
    if os.path.exists('lnurl.png'): #TODO: create new user session
        pass
    else:
        domain = "nostrdvmpwa-89d0c59f417c.herokuapp.com/walletpath"
        auth_url, user, lightninglink = generate_auth_url(domain) # user == k1
        print(f"Generated auth URL: {auth_url}")
        print(lightninglink)
        img = qrcode.make(lightninglink)
        img.save('lnurl.png')
        log_status = False
        save_to_dynamodb(user, log_status)
    try:
        log_status = get_from_dynamodb(user)
    except:
        log_status = False

    if log_status:
        return 'Hell Yeah'
    else:
        return send_file('lnurl.png', mimetype='image/png')
    
@app.route('/walletpath')
def wallet():
    user = request.args.get('k1')
    sig = request.args.get('sig')
    all_params = request.args.to_dict()
    print("All parameters:", all_params)
    if sig is not None:
        response = {"status": "OK"}
        log_status = True
        save_to_dynamodb(user, log_status)
        return jsonify(response)
    else:
        response = {"status": "ERROR", "reason": "error details..."}
        return jsonify(response)

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    # Run Flask app with Gunicorn
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))