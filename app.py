from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/respond', methods=['POST'])
def respond():
    response = request.form.get('response')
    user = request.form.get('user')
    company = request.form.get('company')

    return jsonify(response=response, user=user, company=company)


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)