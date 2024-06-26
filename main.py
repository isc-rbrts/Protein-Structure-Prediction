from flask import Flask, request, redirect, url_for, render_template
import requests
import biotite.structure.io as bsio

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        seq = request.form.get("seq")
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=seq, verify=False)
        pdb_string = response.content.decode('utf-8')

        with open('/tmp/predicted.pdb', 'w') as f:
            f.write(pdb_string)

        structure = bsio.load_structure('/tmp/predicted.pdb', extra_fields=["b_factor"])
        b_value = round(structure.b_factor.mean(), 4)

        return render_template('result.html', data=pdb_string, seq=seq, b_value=b_value)
    
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
