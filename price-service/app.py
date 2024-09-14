from flask import Flask, jsonify
import random

app = Flask(__name__)

cryptos = {
    "bitcoin": 45000,
    "ethereum": 3000,
    "dogecoin": 0.25
}

@app.route('/crypto/<name>', methods=['GET'])
def get_crypto_price(name):
    price = cryptos.get(name.lower(), None)
    if price:
        return jsonify({"crypto": name, "price": price}), 200
    else:
        return jsonify({"message": "Crypto not found"}), 404

@app.route('/cryptos', methods=['GET'])
def get_all_prices():
    return jsonify(cryptos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
