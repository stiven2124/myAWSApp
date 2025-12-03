from flask import Flask, render_template
from routes.login import login_bp
from routes.register import register_bp

app = Flask('__name__')
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)

@app.route('/')
def index():
    return render_template('mypage.html')

if __name__ == '__main__':
    app.run(debug=True)