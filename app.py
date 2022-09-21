from flask import Flask, jsonify, request
import json
from functions import todos_productos, limite_productos

app = Flask(__name__)

@app.route('/mercadolibre', methods=['GET'])

def mercadolibre():
    data = json.loads(request.data)

    if 'limite' not in data:
        titulo, url, precio = todos_productos(data['producto'])
    else:
        titulo, url, precio = limite_productos(data['producto'], data['limite'])

    return jsonify({'datos': {'Título': titulo, 'Enlace': url, 'Precio': precio}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)