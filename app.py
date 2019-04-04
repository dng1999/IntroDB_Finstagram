from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import uuid
import hashlib
import pymysql.cursors
from functools import wraps
import time

app = Flask(__name__)
app.secret_key = "super secret key"
IMAGES_DIR = os.path.join(os.getcwd(), "images")

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             db="finsta",
                             charset="utf8mb4",
                             port=8889,
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if not "username" in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return dec

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html", username=session["username"])

@app.route("/upload", methods=["GET"])
@login_required
def upload():
    query = "SELECT groupName FROM Belong WHERE username=%s"
    with connection.cursor() as cursor:
        cursor.execute(query, (session["username"]))
    data = cursor.fetchall()
    return render_template("upload.html", groupNames = data)

@app.route("/images", methods=["GET"])
@login_required
def images():
    query = "SELECT filePath, photoID FROM Photo WHERE photoOwner=%s OR (filepath, photoID) IN (SELECT filepath, photoID FROM Photo NATURAL JOIN Belong WHERE username=%s) OR (filepath, photoID) IN (SELECT filepath, photoID FROM Follow JOIN Photo ON(photoOwner=followeeUsername) WHERE followerUsername=%s) ORDER BY timestamp DESC"
    with connection.cursor() as cursor:
        cursor.execute(query, (session["username"],session["username"],session["username"]))
    data = cursor.fetchall()

    return render_template("images.html", images=data)

@app.route("/images/<photoID>", methods=["GET"])
def viewImageInfo(photoID):
    query = "SELECT * FROM Photo WHERE photoID=%s"
    with connection.cursor() as cursor:
        cursor.execute(query, (photoID))
    data = cursor.fetchone()

    query = "SELECT displayTimestamp, displayTagged FROM person WHERE username=%s"
    with connection.cursor() as cursor:
        cursor.execute(query, (session["username"]))
    settings = cursor.fetchone()

    query = "SELECT username FROM Tag WHERE photoID=%s AND acceptedTag=1"
    with connection.cursor() as cursor:
        cursor.execute(query, (photoID))
    tags = cursor.fetchall()

    return render_template("viewImage.html", image=data, settings=settings, tags=tags)

@app.route("/image/<image_name>", methods=["GET"])
def image(image_name):
    image_location = os.path.join(IMAGES_DIR, image_name)
    if os.path.isfile(image_location):
        return send_file(image_location, mimetype="image/jpg")

@app.route("/follow", methods=["GET"])
@login_required
def follow():

    query1 = "SELECT * FROM follow WHERE followerUsername=%s and acceptedfollow = 1"
    with connection.cursor() as cursor:
        cursor.execute(query1, (session["username"]))
    followee = cursor.fetchall()
    query2 = "SELECT * FROM follow WHERE followeeUsername=%s and acceptedfollow = 1"
    with connection.cursor() as cursor2:
        cursor2.execute(query2, (session["username"]))
    follower = cursor2.fetchall()
    query3 = "SELECT * FROM follow WHERE followeeUsername=%s and acceptedfollow is NULL"
    with connection.cursor() as cursor3:
        cursor3.execute(query3, (session["username"]))
    waitlist = cursor3.fetchall()
    return render_template("follow.html", followers=follower,followees =followee,waits = waitlist)



@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/loginAuth", methods=["POST"])
def loginAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()

        with connection.cursor() as cursor:
            query = "SELECT * FROM person WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashedPassword ))
        data = cursor.fetchone()
        if data:
            session["username"] = username
            return redirect(url_for("home"))

        error = "Incorrect username or password."
        return render_template("login.html", error=error)

    error = "An unknown error has occurred. Please try again."
    return render_template("login.html", error=error)

@app.route("/registerAuth", methods=["POST"])
def registerAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()
        firstName = requestData["fname"]
        lastName = requestData["lname"]

        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO person (username, password, fname, lname) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username,hashedPassword  , firstName, lastName))
        except pymysql.err.IntegrityError:
            error = "%s is already taken." % (username)
            return render_template('register.html', error=error)

        return redirect(url_for("login"))

@app.route("/searchuser", methods=["POST"])
def searchuser():
    if request.form:
        requestData = request.form
        username = requestData["username"]

        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Follow (followerUsername,followeeUsername,acceptedfollow) VALUES (%s, %s,%s)"
                cursor.execute(query, (session["username"],username,None))
        except pymysql.Error:
            return redirect(url_for("follow"))

        return redirect(url_for("follow"))



@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username")
    return redirect("/")

@app.route("/uploadImage", methods=["POST"])
@login_required
def upload_image():
    if request.files:
        image_file = request.files.get("imageToUpload", "")
        image_name = image_file.filename
        userName = session["username"]
        allFollower = "0"

        filepath = os.path.join(IMAGES_DIR, image_name)
        image_file.save(filepath)
        caption = request.form.get('caption')
        display = request.form.get('display')
        if display == "All Followers":
            allFollower = "1"
        query = "INSERT INTO Photo (photoOwner, timestamp, filePath, caption, allFollowers) VALUES (%s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (userName, time.strftime('%Y-%m-%d %H:%M:%S'), image_name, caption, allFollower))
        message = "Image has been successfully uploaded."


        return render_template("upload.html", message=message)
    else:
        message = "Failed to upload image."
        return render_template("upload.html", message=message)

@app.route("/settings", methods=["GET"])
@login_required
def settings():
    query = "SELECT displayTimestamp, displayTagged FROM person WHERE username=%s"
    with connection.cursor() as cursor:
        cursor.execute(query, (session["username"]))
    data = cursor.fetchone()
    return render_template("settings.html", settings=data)

@app.route("/changeSettings", methods=["POST"])
def changeSettings():
    requestData = request.form
    if (requestData.get("displayTagged")): displayTagged = 1
    else: displayTagged = 0
    if (requestData.get("displayTimestamp")): displayTimestamp = 1
    else: displayTimestamp = 0

    with connection.cursor() as cursor:
        query = "UPDATE person SET displayTagged=%s, displayTimestamp=%s WHERE username=%s"
        cursor.execute(query, (displayTagged, displayTimestamp, session["username"]))

        query = "SELECT displayTagged, displayTimestamp FROM person WHERE username = %s"
        cursor.execute(query, (session["username"]))
        data = cursor.fetchone()
    if (data['displayTagged']==displayTagged and data['displayTimestamp']==displayTimestamp):
        return redirect(url_for("home"))
    else:
        query = "SELECT displayTimestamp, displayTagged FROM person WHERE username=%s"
        with connection.cursor() as cursor:
            cursor.execute(query, (session["username"]))
            data = cursor.fetchone()
        error = "An unknown error has occurred. Please try again."
        return render_template("settings.html", settings=data, error=error)

@app.route('/acceptfollow/<followeruser>',methods = ["POST"])
def acceptf(followeruser):
	with connection.cursor() as cursor:
	    query = 'UPDATE Follow SET acceptedfollow = 1 WHERE followerUsername = %s AND followeeUsername = %s'
	    cursor.execute(query, (followeruser, session["username"]))
	return redirect(url_for('follow'))

@app.route('/declinefollow/<followeruser>',methods = ["POST"])
def declinef(followeruser):
	with connection.cursor() as cursor:
	    query = 'UPDATE Follow SET acceptedfollow = 0 WHERE followerUsername = %s AND followeeUsername = %s'
	    cursor.execute(query, (followeruser, session["username"]))
	return redirect(url_for('follow'))


if __name__ == "__main__":
    if not os.path.isdir("images"):
        os.mkdir(IMAGES_DIR)
    app.run()
