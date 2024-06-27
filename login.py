from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Replace with actual authentication logic
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')
