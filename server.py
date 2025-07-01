from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)


@app.route('/index.html')
def index():
    return render_template('index.html', name=None)


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        name = data['name']
        message = data['message']
        file = database.write(f'\n{email},{name},{message}')


def write_to_csv(data):
    file_exists = os.path.isfile('database.csv')
    with open('database.csv', mode='a', newline='') as csvfile:
        email = data['email']
        name = data['name']
        message = data['message']

        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if not file_exists:
            csv_writer.writerow(['email', 'name', 'message'])

        csv_writer.writerow([email, name, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/index.html')
    else:
        return 'something went wrong try again'


if __name__ == '__main__':
    app.run(debug=True)
