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
    query = "SELECT groupName, groupOwner FROM Belong WHERE username=%s"
    with connection.cursor() as cursor:
        cursor.execute(query, (session["username"]))
    data = cursor.fetchall()
    return render_template("upload.html", groups = data)

@app.route("/images", methods=["GET"])
@login_required
def images():
    queriesWUserName = [];
    queriesWUserName.append( "CREATE VIEW self AS SELECT filePath, photoID, timestamp FROM Photo WHERE photoOwner=%s")
    queriesWUserName.append("CREATE VIEW groups AS SELECT filePath, photoID, timestamp FROM Photo JOIN Belong USING (groupName, groupOwner) WHERE Belong.username = %s")
    queriesWUserName.append( "CREATE VIEW following AS SELECT filePath, photoID, timestamp FROM Follow JOIN Photo ON(photoOwner=followeeUsername) WHERE followerUsername = %s AND allFollowers = '1' AND acceptedFollow = 1")
    query= "SELECT DISTINCT filePath, photoID, timestamp FROM (SELECT filePath, photoID, timestamp FROM self UNION ALL SELECT filePath, photoID, timestamp FROM groups UNION ALL SELECT filePath, photoID,timestamp FROM following)AS T ORDER BY timestamp DESC"
    with connection.cursor() as cursor:
        for i in range (len(queriesWUserName)):
            cursor.execute(queriesWUserName[i], session["username"])
        cursor.execute(query)
        data = cursor.fetchall()
        query = "DROP VIEW self, groups, following"
        cursor.execute(query)

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

    return render_template("viewImage.html", image=data, settings=settings, tags=tags, session=session["username"])

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
        else:
            result = display.split(",")
            groupName = result[0].split(":")[1]
            groupOwner = result[1].split(":")[1]
            query = "INSERT INTO Photo (photoOwner, timestamp, filePath, caption, allFollowers, groupName, groupOwner) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(query, (userName, time.strftime('%Y-%m-%d %H:%M:%S'), image_name, caption, allFollower,groupName, groupOwner))

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

@app.route('/editImage/<photoID>',methods = ["GET"])
def editImage(photoID):
    query = "SELECT * FROM Photo WHERE photoID=%s"
    with connection.cursor() as cursor:
        cursor.execute(query, (photoID))
    data = cursor.fetchone()

    query = "SELECT username FROM Tag WHERE photoID=%s AND (acceptedTag IS NULL OR acceptedTag = 1)"
    with connection.cursor() as cursor:
        cursor.execute(query, (photoID))
    tags = cursor.fetchall()

    return render_template("editImage.html", image=data, tags=tags)

@app.route('/saveCaption/<photoID>',methods = ["POST"])
def saveCaption(photoID):
    if request.form:
        requestData = request.form
        caption = requestData["caption"]

        query = "UPDATE Photo SET caption=%s WHERE photoID=%s"
        with connection.cursor() as cursor:
            cursor.execute(query, (caption, photoID))

    return redirect(url_for('editImage', photoID=photoID))

@app.route('/removeTag/<photoID>/<username>',methods = ["GET"])
def removeTag(photoID, username):
    query = "DELETE FROM Tag WHERE photoID=%s AND username=%s AND acceptedTag is NULL"
    with connection.cursor() as cursor:
        cursor.execute(query, (photoID, username))

    return redirect(url_for('editImage', photoID=photoID))

@app.route('/addTag/<photoID>',methods = ["GET"])
def addTag(photoID):
    username = request.args.get("addTag")
    if (username != ''):
        try:
            query = "INSERT INTO Tag (username, photoID,acceptedTag) VALUES (%s, %s,%s)"
            with connection.cursor() as cursor:
                cursor.execute(query, (username, photoID,None))
        except pymysql.err.IntegrityError:
            return redirect(url_for('editImage', photoID=photoID))

    return redirect(url_for('editImage', photoID=photoID))

@app.route('/deleteImage/<photoID>',methods = ["GET"])
def deleteImage(photoID):
    query = "DELETE FROM Photo WHERE photoID=%s"
    with connection.cursor() as cursor:
        cursor.execute(query, (photoID))

    return redirect(url_for('images'))

@app.route("/tag", methods=["GET"])
@login_required
def tag():
    query1 = "SELECT * FROM Photo JOIN Tag using (photoID) WHERE Tag.username = %s and acceptedTag = 1"
    with connection.cursor() as cursor:
        cursor.execute(query1, (session["username"]))
    data = cursor.fetchall()
    query2 = "SELECT * FROM Photo JOIN Tag using (photoID) WHERE Tag.username=%s and acceptedtag is NULL"
    with connection.cursor() as cursor2:
        cursor2.execute(query2, (session["username"]))
    waiting = cursor2.fetchall()
    query = "SELECT username FROM Tag WHERE photoID=%s AND acceptedTag=1"
    return render_template("tag.html", images = data, waitlist = waiting)

@app.route('/accepttag/<photoID>',methods = ["POST"])
@login_required
def acceptt(photoID):
    with connection.cursor() as cursor:
        query = 'UPDATE Tag SET acceptedtag = 1 WHERE photoID = %s and username = %s'
        cursor.execute(query, (photoID, session["username"]))
    return redirect(url_for('tag'))

@app.route('/declinetag/<photoID>',methods = ["POST"])
@login_required
def declinet(photoID):
    with connection.cursor() as cursor:
        query = 'UPDATE Tag SET acceptedtag = 0 WHERE photoID = %s AND username= %s'
        cursor.execute(query, (photoID, session["username"]))
    return redirect(url_for('tag'))
@app.route('/unfollow/<followeeuser>',methods = ["POST"])
@login_required
def unfollow(followeeuser):
    with connection.cursor() as cursor:
        query = 'Delete FROM Follow WHERE followeeUsername = %s AND followerUsername = %s'
        cursor.execute(query, (followeeuser, session["username"]))
#    with connection.cursor() as cursor:
#        query = 'CREATE VIEW pair AS SELECT * FROM Tag NATURAL JOIN Photo where photoOwner = %s and username = %s'
#        cursor.execute(query, (followeeuser, session["username"]))
#    with connection.cursor() as cursor:
#        query = 'SELECT photoID from pair'
#        cursor.execute(query)
#    data = cursor.fetchall()
#    with connection.cursor() as cursor:
#        query = 'DROP VIEW pair'
#        cursor.execute(query)
#    with connection.cursor() as cursor:
#        for item in data:
#            query = 'UPDATE Tag SET acceptedTag = 0 WHERE photoID = %s and username = %s'
#            cursor.execute(query,(item['photoID'],session["username"]))

    return redirect(url_for('follow'))

@app.route('/searchtag',methods = ["POST"])
@login_required
def searchtag():
    if request.form:
        requestData = request.form
        username = requestData["username"]
    try:
        queriesWUserName = [];
        queriesWUserName.append( "CREATE VIEW self AS SELECT filePath, photoID, timestamp FROM Photo WHERE photoOwner=%s")
        queriesWUserName.append("CREATE VIEW groups AS SELECT filePath, photoID, timestamp FROM Photo JOIN Belong USING (groupName, groupOwner) WHERE Belong.username = %s")
        queriesWUserName.append( "CREATE VIEW following AS SELECT filePath, photoID, timestamp FROM Follow JOIN Photo ON(photoOwner=followeeUsername) WHERE followerUsername = %s AND allFollowers = '1' AND acceptedFollow = 1")
        query= "SELECT * FROM (SELECT * FROM self UNION ALL SELECT filePath, photoID, timestamp FROM groups UNION ALL SELECT filePath, photoID,timestamp FROM following)AS T ORDER BY timestamp DESC"
        data2 =[]
        
        with connection.cursor() as cursor:
            for i in range (len(queriesWUserName)):
                cursor.execute(queriesWUserName[i], session["username"])
            cursor.execute(query)
            data = cursor.fetchall()
            query = "DROP VIEW self, groups, following"
            cursor.execute(query)
        query1 = "SELECT * FROM Photo JOIN Tag using (photoID) WHERE Tag.username = %s and acceptedTag = 1"
        with connection.cursor() as cursor:
            cursor.execute(query1, (session["username"]))
        data4 = cursor.fetchall()
        for item in data4:
            if item not in data:
                data.append(item)
        with connection.cursor() as cursor:
            query3 = "SELECT photoID FROM Photo JOIN Tag using (photoID) WHERE Tag.username = %s and acceptedTag = 1"
            cursor.execute(query3, username)
        data3 = cursor.fetchall()
        lst = []
        print(data3)
        print(data)
        for item in data3:
            for values in data:
                if item['photoID'] == values['photoID']:
                    if item['photoID'] not in lst:
                        lst.append(item['photoID'])
        query3 = "SELECT * FROM Photo NATURAL JOIN Tag WHERE photoID = %s and acceptedTag = 1 and username = %s"
        with connection.cursor() as cursor:
            for i in range(len(lst)):
                cursor.execute(query3,(lst[i],username))
                data5 = cursor.fetchall()
                data2.extend(data5)
    except pymysql.Error:
        return redirect(url_for("tag"))
    return render_template("searchtag.html",images = data2,user = username)


if __name__ == "__main__":
    if not os.path.isdir("images"):
        os.mkdir(IMAGES_DIR)
    app.run()
