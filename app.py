from flask import Flask, render_template, request, session, redirect, url_for
import pyrebase

app = Flask(__name__)


config = {
    "apiKey": "AIzaSyCPrZZdVIa72dHvGIN020834wfVRmhR-I4",
    "authDomain": "lokaverk-17eb5.firebaseapp.com",
    "databaseURL": "https://lokaverk-17eb5.firebaseio.com",
    "projectId": "lokaverk-17eb5",
    "storageBucket": "lokaverk-17eb5.appspot.com",
    "messagingSenderId": "166815552679",
    "appId": "1:166815552679:web:0847c391d9f1241ae23782",
    "measurementId": "G-VYQPF38Z5M"
}


fb = pyrebase.initialize_app(config)
db = fb.database()
# innsetning db til að fá dálkana keyra bara einu sinni
#db.child("bill").push({"nr":"abc12", "tegund":"Volvo","utegund":"Lungo", "argerd":"2020","akstur":"1500"})


@app.route("/")
def index():
    u = db.child("bill").get.val()
    lst = list(u.items())

    return render_template("index.html", bilar=lst)
@app.route("/bill/<id>")
def bill(id):
    b = db.child("bill").child(id).get().val()
    bill = list(b.items())
    return render_template("car.html", bill = bill, id=id)

@app.route("/innskra", methods=["GET","POST"])
def innskra():

    u = db.child("bill").get.val()
    lst = list(u.items())

    return render_template("innskra.html", bilar=lst)

@app.route("/nyskra")  #vantaði /
def nyskra():
    return render_template("register.html")

@app.route("/donyskra", methods=["GET","POST"])
def doregister():
    skrnr = []
    if request.method == "POST":
        nr = request.form["nr"]
        tegund = request.form["tegund"]
        utegund = request.form["utegund"]
        argerd = request.form["argerd"]
        akstur = request.form["akstur"]


        u = db.child("bill").get().val()
        lst = list(u.items())
        for i in lst:
            skrnr.append(i[1]["nr"])

        if nr not in skrnr:
            db.child("bill").push({"nr":nr,"tegund":tegund,"utegund":utegund,"argerd":argerd,"akstur":akstur})
            return render_template("registered.html", nr = nr)
        else:
            return render_template("userexists.html", nr = nr)
    else:
        return render_template("no_method.html")
@app.route("/breytaeyda", methods=["POST"])
def breytaeyda():
    if request.method == "POST":
        if request.form["submit"] == "eyda":
            db.child("bill").child(request.form["id"]).remove()
            return render_template("deleted.html", nr = request.form["nr"])
        else:
            db.child("bill").child(request.form["id"]).update({"nr":request.form["nr"],"tegund":request.form["tegund"], "utegund":request.form["utegund"], "argerd":request.form["argerd"],"akstur":request.form["akstur"]})
            return render_template("updated.html", nr = request.form["nr"])
    else:
        return render_template("no_method.html")

# það þarf alltaf að ræsa appið

if __name__ == "__main__":
	app.run(debug=True)