from flask import Flask, render_template, request, redirect, url_for
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'mongundial'
mongo = PyMongo(app)


@app.route('/')
def home_page():
    online_users = mongo.db.user.find({'online': True})
    return render_template('index.html',
        online_users=online_users)

@app.route('/u/')
def users():
    users = mongo.db.user.find()
    return render_template('users.html',
                           users=users)

@app.route('/u/<userid>')
def user_profile(userid):
    user = mongo.db.user.find_one({"_id": ObjectId(userid)})
    return render_template('user.html',
        user=user)

@app.route('/u/delete/<userid>')
def user_profile_delete(userid):
    user = mongo.db.user.find_one({"_id": ObjectId(userid)})
    mongo.db.user.remove(user)
    return redirect(url_for('users'))

@app.route('/u/create', methods=["POST", "GET"])
def user_profile_create():
    if request.method == "POST":
        data_user = {'nombre':request.form["name"],
                     'edad':request.form["edad"]}

        uid = mongo.db.user.insert(data_user)
        return redirect(url_for('user_profile', userid=uid))
    return render_template('user_edit.html',
                           user={})


@app.route('/u/edit/<userid>', methods=["POST", "GET"])
def user_profile_edit(userid):
    user = mongo.db.user.find_one({"_id": ObjectId(userid)})
    
    if request.method == "POST":
        data_user = {'nombre':request.form["name"],
                     'edad':request.form["edad"]}

        user.update(data_user)
        mongo.db.user.save(user)
        return redirect(url_for('user_profile', userid=user["_id"]))
    return render_template('user_edit.html',
        user=user)

@app.route('/resultados')
def tarjeta():
    data = {'grupos':GRUPOS, 'tarjeta':GRUPOS}
    return render_template('tarjeta.html', data=data)

GRUPOS = {
    'A':{
        'a1': {
            'A':'Brasil', 
            'B':'Croacia', 
            'fecha':1 },
        'a2': {
            'A':'Mexico',
            'B':'Camerun',
            'fecha':2 }
    }, 
    'B': {
        'b1': {
            'A':'Esp', 
            'B':'PB', 
            'fecha':1 },
        'b2': {
            'A':'Chile',
            'B':'Australia',
            'fecha':2 }
    }
   }

           


if __name__ == "__main__":
    app.run(debug=True)
