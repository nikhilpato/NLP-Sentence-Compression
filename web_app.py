from flask import Flask, request, render_template
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z]/'


@app.route('/')
def my_form():
    return render_template('home_template.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form.get('textbox')
    return render_template('home_template.html', short_sent = text)


if __name__ == '__main__':
    app.run(debug=True)
