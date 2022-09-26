from flask import Flask, jsonify, request, render_template, Response
import json
from functions import todos_productos, limite_productos
import requests

app = Flask(__name__)

@app.route('/mercadolibre', methods=['GET'])

def mercadolibre():
    data = json.loads(request.data)

    if 'limite' not in data:
        titulo, url, precio = todos_productos(data['producto'])
    else:
        titulo, url, precio = limite_productos(data['producto'], data['limite'])

    return jsonify({'datos': {'titulo': titulo, 'enlace': url, 'precio': precio}})


@app.route('/descargarinfo', methods=['GET', 'POST'])


def descargarinfo():
    if request.method == 'POST':
        
        producto = request.form['producto']
        limite = request.form['limite']

        r = requests.get('http://127.0.0.1:5000/mercadolibre', json={'producto': producto, 'limite': int(limite)})

        if r.status_code == 200:
            data = json.loads(r.text)

            texto = ""

            for t, p, e in zip( data['datos']['titulo'], data['datos']['precio'], data['datos']['enlace']):
                texto += f'{t}|{p}|{e}\n'

            return Response(
                texto,
                mimetype="text",
                headers={
                    "Content-disposition":"attachment; filename=datos.txt"
                }
            )

            # print(data)
        else:
            return 'Error'

        # print(producto, limite)
        # return {'asd': 'asddsfsd'}

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


