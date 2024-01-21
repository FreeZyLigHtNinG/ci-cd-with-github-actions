from flask import Flask, request, render_template, redirect, url_for
import os
import subprocess

app = Flask(__name__)

# In-memory database
items = []


@app.route('/staging', methods=['POST'])
def staging():
    payload = request.json
    ref = payload.get('ref', '')
    response = ('', 204)
    if ref == 'refs/heads/staging':
        os.system("git pull origin staging")
        os.system("pip3 install -r requirements.txt")
        os.system("python -m unittest test-app.py")
        os.system("python test-endtoend-app.py")
        response = 'Test run successfuly'
    return response


@app.route('/deploy', methods=['POST'])
def deploy():
    payload = request.json
    ref = payload.get('ref', '')
    response = ('', 204)
    if ref == 'refs/heads/main':
        try :
            if app.pid :
                os.kill(app_pid, 15)
            os.system("git pull origin main")
            os.system("pip3 install -r requirements.txt")
            app_process = subprocess.Popen(['python', 'app.py'])
            app_pid = app_process.pid
            response = 'App running'
        except Exception as e:
            response = f'Error during deployment: {str(e)}'
    return response


@app.route('/')
def index():
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    item = request.form.get('item')
    if item:
        items.append(item)
    return redirect(url_for('index'))


@app.route('/delete/<int:index>')
def delete_item(index):
    if index < len(items):
        items.pop(index)
    return redirect(url_for('index'))


@app.route('/update/<int:index>', methods=['POST'])
def update_item(index):
    if index < len(items):
        items[index] = request.form.get('new_item')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

#ttt