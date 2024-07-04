from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/transaction/transaction.html')

from transaction.view import transaction_blueprint
from smartContract.view import smartContract_blueprint
from address.view import address_blueprint


app.register_blueprint(transaction_blueprint)
app.register_blueprint(smartContract_blueprint)
app.register_blueprint(address_blueprint)


if __name__ == '__main__':
    app.run(port=5008,host='0.0.0.0')