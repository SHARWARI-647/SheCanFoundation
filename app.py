
from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

# -------------------------------
# Database Connection Function
# -------------------------------

def get_db_connection():

    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="shecanfoundation",
        cursorclass=pymysql.cursors.DictCursor
    )


# -------------------------------
# Home Page
# -------------------------------

@app.route('/')
def home():

    return render_template('index.html')


# -------------------------------
# Submit Contact Form
# -------------------------------

@app.route('/contact', methods=['POST'])
def contact():

    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']
    subject = request.form['subject']
    message = request.form['message']

    db = get_db_connection()

    cursor = db.cursor()

    query = """
    INSERT INTO contact_messages
    (fullname, email, phone, subject, message)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        fullname,
        email,
        phone,
        subject,
        message
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return redirect('/success')


# -------------------------------
# Success Page
# -------------------------------

@app.route('/success')
def success():

    return render_template('success.html')


# -------------------------------
# Admin Dashboard
# -------------------------------

@app.route('/admin')
def admin():

    db = get_db_connection()

    cursor = db.cursor()

    query = """
    SELECT * FROM contact_messages
    ORDER BY id DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'admin.html',
        messages=data
    )


# -------------------------------
# Reply to User
# -------------------------------

@app.route('/reply/<int:id>', methods=['POST'])
def reply(id):

    admin_reply = request.form['reply']

    db = get_db_connection()

    cursor = db.cursor()

    query = """
    UPDATE contact_messages
    SET admin_reply = %s,
        status = 'Replied'
    WHERE id = %s
    """

    cursor.execute(
        query,
        (admin_reply, id)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect('/admin')


# -------------------------------
# Delete Message
# -------------------------------

@app.route('/delete/<int:id>')
def delete(id):

    db = get_db_connection()

    cursor = db.cursor()

    query = """
    DELETE FROM contact_messages
    WHERE id = %s
    """

    cursor.execute(query, (id))

    db.commit()

    cursor.close()
    db.close()

    return redirect('/admin')


# -------------------------------
# User Response Page
# -------------------------------

@app.route('/responses')
def responses():

    db = get_db_connection()

    cursor = db.cursor()

    query = """
    SELECT * FROM contact_messages
    ORDER BY id DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'responses.html',
        messages=data
    )


# -------------------------------
# Run Flask App
# -------------------------------

if __name__ == '__main__':

    app.run(debug=True)
