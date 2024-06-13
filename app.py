from flask import Flask, render_template, request, redirect, url_for, flash
import os
from encryption_utils import store_data, access_data, modify_data

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        secret_code = request.form['secret_code']
        data = request.form['data']
        success = store_data(secret_code, data)
        if success:
            flash('Secret code and data stored securely.', 'success')
        else:
            flash('Error storing data.', 'danger')
        return redirect(url_for('index'))
    return render_template('store.html')

@app.route('/access', methods=['GET', 'POST'])
def access():
    if request.method == 'POST':
        secret_code = request.form['secret_code']
        data = access_data(secret_code)
        if data:
            return render_template('access.html', data=data)
        else:
            flash('Access denied. Incorrect secret code or error accessing data.', 'danger')
            return redirect(url_for('index'))
    return render_template('access.html')

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        secret_code = request.form['secret_code']
        new_data = request.form['new_data']
        success = modify_data(secret_code, new_data)
        if success:
            flash('Data modified successfully.', 'success')
        else:
            flash('Access denied. Incorrect secret code or error modifying data.', 'danger')
        return redirect(url_for('index'))
    return render_template('modify.html')

if __name__ == '__main__':
    app.run(debug=True)
