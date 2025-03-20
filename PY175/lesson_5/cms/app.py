from flask import Flask, render_template, send_from_directory, flash, request, url_for, redirect
from markdown import markdown
import os

app = Flask(__name__)
app.secret_key = 'secret1'

def get_file_path(file_name):
    return os.path.join(get_data_directory(), file_name)

def get_data_directory():
    if app.config['TESTING']:
        return os.path.join(os.path.dirname(__file__), 'tests', 'data')
    else:
        return os.path.join(os.path.dirname(__file__), 'data')

@app.route('/')
def index():
    data_dir = get_data_directory()
    files = [os.path.basename(path) for path in os.listdir(data_dir)]
    return render_template('index.html', files=files)

@app.route('/<file_name>')
def open_file(file_name):
    data_dir = get_data_directory()
    file_path = get_file_path(file_name)

    if os.path.isfile(file_path):
        if(file_name[-3:] == ".md"):
            with open(file_path, "r") as f:
                markdown_text = f.read()
            return render_template('markdown.html', content=markdown(markdown_text))

        return send_from_directory(data_dir, file_name)
    else:
        flash(f"{file_name} does not exist.")
        return redirect(url_for('index'))

@app.route('/<file_name>/edit')
def edit_file(file_name):
    file_path = get_file_path(file_name)
    
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            content = f.read()

        return render_template('edit.html', file_name=file_name, content=content)
    else:
        flash(f"{file_name} does not exist.")
        return redirect(url_for('index'))

@app.route('/<file_name>/save', methods=["POST"])
def save_file(file_name):
    content = request.form['content']
    file_path = get_file_path(file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    flash(f'{file_name} has been updated.', "success")
    return redirect(url_for('index'))

@app.route('/new')
def new_file():
    return render_template('new.html')

@app.route('/new', methods=["POST"])
def create_new_file():
    file_name = request.form.get('file_name', '').strip()
    file_path = get_file_path(file_name)
    if len(file_name) == 0:
        flash("A name is required.")
        return render_template('new.html'), 422
    elif os.path.exists(file_path):
        flash(f"{file_name} already exists.")
        return render_template('new.html'), 422
    else:
        with open(file_path, 'w') as file:
            file.write("")
        flash(f"{file_name} has been created.", "success")
        return redirect(url_for('index'))
    
@app.route('/<file_name>/delete', methods=["POST"])
def delete_file(file_name):
    file_path = get_file_path(file_name)

    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file
        flash(f'{file_name} has been deleted.', 'success')
    else:
        flash(f"{file_name} doesn't exist")
    return redirect(url_for('index'))

@app.route('/users/signin')
def go_to_sign_in():
    return render_template('sign_in.html')

@app.route('/users/signin', methods=["POST"])
def sign_in():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if (username == 'admin' and password == 'secret'):
        flash('Welcome!', 'success')
        return redirect(url_for('index'))
    
    flash('Incorrrect username or password', 'error')
    return render_template('sign_in.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003)