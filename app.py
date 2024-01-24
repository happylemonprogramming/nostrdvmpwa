from flask import Flask, render_template, send_file, request
from lightninglogin import generate_auth_url
import qrcode
import os

app = Flask(__name__, template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html', streamlit_url=os.environ.get('streamlit_url'))

@app.route('/lightninglogin')
def login():
    signature = request.args.get('sig')

    # Example usage
    domain = "nostrdvmpwa-89d0c59f417c.herokuapp.com/lightninglogin"
    auth_url, k1, lightninglink = generate_auth_url(domain)
    print(f"Generated auth URL: {auth_url}")
    print(lightninglink)
    img = qrcode.make(lightninglink)
    img.save('lnurl.png')

    if signature is not None:
        return 'Hell Yeah'
    else:
        return send_file('lnurl.png', mimetype='image/png')

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    # Run Flask app with Gunicorn
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))