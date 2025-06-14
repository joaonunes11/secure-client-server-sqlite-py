"""
Aplicacoes Distribuidas - Projeto 3 - server.py
Grupo: 14
Numeros de aluno: 53299
"""

from flask import Flask, request, make_response, g, jsonify, redirect, session
from requests_oauthlib import OAuth2Session
import contextlib
import ssl
import sqlite3
import json
from os.path import isfile

import os

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('../certs/server.crt',
                        keyfile='../certs/CA.key')
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations = '../certs/'

app = Flask(__name__)


# # Informação da aplicação registada no GitHub
client_id = "136ab04f3500a4831585"
client_secret = "a9acad9be57884872b9ef3ba68dfcbd9214b2ca9"
# Informação sobre a Authorization server
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


def connect_db():
    db_is_created = isfile('ad14.db')
    connection = sqlite3.connect('ad14.db')
    if not db_is_created:
        init_db()
        print('Initialized the database.')
    return connection


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Closes the database again at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with app.open_resource('ad14.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.cursor().execute('PRAGMA foreign_keys = ON')
    db.commit()


def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def listToDict(lstA, lstB):
    result = {}
    for t in lstB:
        zippedLst = zip(lstA, t)
        result[t[0]] = dict(zippedLst)
    return result


with app.app_context():
    connect_db()


# @app.route("/")
# def login():
#     github = OAuth2Session(client_id)

#     authorization_url, state = github.authorization_url(authorization_base_url)
#     # State is used to prevent CSRF, keep this for later.
#     session['oauth_state'] = state
#     return redirect(authorization_url)


# @app.route("/callback", methods=["GET"])
# def callback():
#     github = OAuth2Session(client_id, state=session['oauth_state'])
#     token = github.fetch_token(token_url,
#                                client_secret=client_secret,
#                                authorization_response=request.url)
#     session['oauth_token'] = token
#     return redirect('.profile')


@app.route('/utilizadores', methods=['POST'])
@app.route('/utilizadores/<int:id>', methods=['GET', 'DELETE', 'PUT'])
@app.route('/utilizadores/rate', methods=['POST'])
@app.route('/utilizadores/all', methods=['GET', 'DELETE'])
def utilizadores(id=None):
    # SHOW
    if request.method == 'GET':
        # SHOW USER
        if request.url == 'https://localhost:5000/utilizadores/' + str(id):
            user = query_db(
                "SELECT * FROM utilizadores WHERE id=?", [id])

            listKeys = ['id']
            result = listToDict(listKeys, user)

            if len(user) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response("not found!")
                r.status_code = 404
            return r

        # SHOW USERS
        elif request.url == 'https://localhost:5000/utilizadores/all':
            users = query_db(
                "SELECT * FROM utilizadores")

            listKeys = ['id', 'nome', 'username', 'password']
            result = listToDict(listKeys, users)

            if len(users) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response("not found!")
                r.status_code = 404

            return r

    # REMOVE
    elif request.method == 'DELETE':
        # REMOVE USER
        if request.url == 'https://localhost:5000/utilizadores/' + str(id):
            user = query_db(
                "SELECT * FROM utilizadores WHERE id=?", [int(id)], one=True)

            if len(user) > 0:
                delete = query_db(
                    "DELETE FROM utilizadores WHERE id=?", [int(id)], one=True)
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

        # REMOVE USERS
        if request.url == 'https://localhost:5000/utilizadores/all':
            users = query_db(
                "SELECT * FROM utilizadores")

            if len(users) > 0:
                delete = query_db(
                    "DELETE FROM utilizadores")
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r
    # ADD
    elif request.method == 'POST':
        # ADD USER
        if request.url == 'https://localhost:5000/utilizadores':
            data = json.loads(request.data)

            users = query_db(
                "INSERT INTO utilizadores (nome, username, password) VALUES(?, ?, ?)", [data['nome'], data['username'], data['password']])
            user_id = query_db(
                "SELECT id FROM utilizadores WHERE username=?", [data['username']], one=True)

            r = make_response(
                json.dumps("inserted {}".format(user_id[0])))
            r.status_code = 201
            r.headers['location'] = 'utilizadores/' + str(user_id[0])
            return r.headers['location']

        # ADD USER RATE
        elif request.url == 'https://localhost:5000/utilizadores/rate':
            data = json.loads(request.data)
            rate_id = query_db(
                "SELECT id FROM rates WHERE sigla=", [data['rate']], one=True)

            rate = query_db(
                "INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES(?, ?, ?)", [data['id_user'], data['id_album'], rate_id[0]])

            r = make_response(json.dumps("rate %s added!" % data['rate']))
            r.status_code = 201
            r.headers['location'] = '/utilizadores/rate/' + str(data['rate'])
            return r

    # UPDATE
    elif request.method == 'PUT':

        if request.url == 'https://localhost:5000/utilizadores/' + str(id):
            data = json.loads(request.data)
            check_user = query_db(
                "SELECT * FROM utilizadores WHERE id=?", [data['id_user']])

            if len(check_user) > 0:
                update = query_db(
                    "UPDATE utilizadores SET password=? WHERE id = ?", [data['id_user'], data['password']])
                r = make_response("UPDATE {} success!".format(data['id_user']))
                r.status_code = 200
            else:
                r = make_response("UPDATE {} failed!".format(data['id_user']))
                r.status_code = 204

            return r

# ----------------------------------------------------------------------
@app.route('/bandas', methods=['POST'])
@app.route('/bandas/<int:id>', methods=['GET', 'DELETE'])
@app.route('/bandas/all', methods=['GET', 'DELETE'])
def bandas(id=None):

    # SHOW
    if request.method == 'GET':

        # SHOW BANDA
        if request.url == 'https://localhost:5000/bandas/' + str(id):
            banda = query_db(
                "SELECT * FROM bandas WHERE id=?", [id], one=True)

            listKeys = ['id']
            result = listToDict(listKeys, banda)

            if len(banda) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response("not found!")
                r.status_code = 404
            return r

        # SHOW BANDAS
        elif request.url == 'https://localhost:5000/bandas/all':
            bandas = query_db(
                "SELECT * FROM bandas")

            listKeys = ['id', 'nome', 'ano', 'genero']
            result = listToDict(listKeys, bandas)

            if len(bandas) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response("not found!")
                r.status_code = 404

            return r

    # REMOVE
    elif request.method == 'DELETE':

        # REMOVE BANDA
        if request.url == 'https://localhost:5000/bandas/' + str(id):
            banda = query_db(
                "SELECT * FROM bandas WHERE id=?", [int(id)], one=True)

            if len(banda) > 0:
                delete = query_db(
                    "DELETE FROM bandas WHERE id=?", [int(id)], one=True)
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

        # REMOVE BANDAS
        if request.url == 'https://localhost:5000/bandas/all':
            bandas = query_db(
                "SELECT * FROM bandas")

            if len(bandas) > 0:
                delete = query_db(
                    "DELETE FROM bandas")
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

    # ADD
    elif request.method == 'POST':

        # ADD BAND
        if request.url == 'https://localhost:5000/bandas':
            data = json.loads(request.data)

            bandas = query_db(
                "INSERT INTO bandas (nome, ano, genero) VALUES(?, ?, ?)", [data['nome'], data['ano'], data['genero']])
            banda_id = query_db(
                "SELECT id FROM bandas WHERE nome=?", [data['nome']], one=True)

            r = make_response(
                json.dumps("inserted {}".format(banda_id[0])))
            r.status_code = 201
            r.headers['location'] = 'bandas/' + str(banda_id[0])
            return r.headers['location']


# ----------------------------------------------------------------------
@app.route('/albuns', methods=['POST'])
@app.route('/albuns/<int:id>', methods=['GET', 'DELETE', 'PUT'])
@app.route('/albuns/all', methods=['GET', 'DELETE'])
@app.route('/albuns/banda/<int:id>', methods=['GET', 'DELETE'])
@app.route('/albuns/utilizador/<int:id>', methods=['GET', 'DELETE'])
@app.route('/albuns/rate/<int:id>', methods=['GET', 'DELETE'])
def albuns(id=None):
    if request.method == 'POST':

        # ADD ALBUM
        if request.url == 'https://localhost:5000/albuns':
            data = json.loads(request.data)

            albuns = query_db(
                "INSERT INTO albuns (id_banda, nome, ano_album) VALUES(?, ?, ?)", [data['id_banda'], data['nome'], data['ano_album']])
            album_id = query_db(
                "SELECT id FROM albuns WHERE nome=?", [data['nome']], one=True)

            r = make_response(
                json.dumps("inserted {}".format(album_id[0])))
            r.status_code = 201
            r.headers['location'] = 'albuns/' + str(album_id[0])
            return r.headers['location']

    # SHOW
    elif request.method == 'GET':

        # SHOW ALBUM
        if request.url == 'https://localhost:5000/albuns/' + str(id):
            album = query_db(
                "SELECT * FROM albuns WHERE id=?", [id], one=True)

            listKeys = ['id']
            result = listToDict(listKeys, album)

            if len(album) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response("not found!")
                r.status_code = 404
            return r

        # SHOW ALBUNS
        elif request.url == 'https://localhost:5000/albuns/all':
            albuns = query_db(
                "SELECT * FROM albuns")

            listKeys = ['id', 'id_banda', 'nome', 'ano_album']
            result = listToDict(listKeys, albuns)

            if len(albuns) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response("not found!")
                r.status_code = 404

            return r

        # SHOW ALBUNS BANDA
        elif request.url == 'https://localhost:5000/albuns/banda/' + str(id):
            albuns = query_db(
                "SELECT * FROM albuns WHERE id_banda=?", [int(id)])
            listKeys = ['id', 'id_banda', 'nome', 'ano_album']
            result = listToDict(listKeys, albuns)

            if len(albuns) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response("not found!")
                r.status_code = 404

            return r

        # SHOW ALBUNS UTILIZADOR
        elif request.url == 'https://localhost:5000/albuns/utilizador/' + str(id):
            albuns = query_db(
                "SELECT * FROM albuns WHERE id in(SELECT id_album FROM listas_albuns WHERE id_user=(SELECT id FROM utilizadores WHERE id=?))", [int(id)])

            listKeys = ['id', 'id_banda', 'nome', 'ano_album']
            result = listToDict(listKeys, albuns)

            if len(albuns) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 404

            return r

        # SHOW ALBUNS RATE
        elif request.url == 'https://localhost:500/albuns/rate/' + str(id):
            albuns = query_db(
                "SELECT * FROM albuns WHERE id in(SELECT id_album FROM listas_albuns WHERE id_rate=?)", [int(id)])

            listKeys = ['id', 'id_banda', 'nome', 'ano_album']
            result = listToDict(listKeys, albuns)

            if len(albuns) > 0:
                r = make_response(json.dumps(result))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 404

            return r

    # REMOVE
    elif request.method == 'DELETE':

        # REMOVE ALBUM
        if request.url == 'https://localhost:5000/albuns/' + str(id):
            album = query_db(
                "SELECT * FROM albuns WHERE id=?", [int(id)], one=True)

            if len(album) > 0:
                delete = query_db(
                    "DELETE FROM albuns WHERE id=?", [int(id)], one=True)
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

        # REMOVE ALBUNS
        elif request.url == 'https://localhost:5000/albuns/all':
            albuns = query_db(
                "SELECT * FROM albuns")

            if len(albuns) > 0:
                delete = query_db(
                    "DELETE FROM albuns")
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

        # REMOVE BANDA ALBUNS
        elif request.url == 'https://localhost:5000/albuns/banda/' + str(id):
            albuns = query_db(
                "SELECT * FROM albuns WHERE id_banda=?", [int(id)])

            if len(albuns) > 0:
                delete = query_db(
                    "DELETE FROM albuns WHERE id_banda=?", [int(id)])
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

        # REMOVE UTILIZADOR ALBUNS
        elif request.url == 'https://localhost:5000/albuns/utilizador/' + str(id):
            albuns = query_db(
                "SELECT * FROM albuns WHERE id in(SELECT id_album FROM listas_albuns WHERE id_user=(SELECT id FROM utilizadores WHERE id=?))", [int(id)])

            if len(albuns) > 0:
                delete = query_db(
                    "DELETE FROM albuns WHERE id in(SELECT id_album FROM listas_albuns WHERE id_user=(SELECT id FROM utilizadores WHERE id=?))", [int(id)])
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

        # REMOVE ALBUNS RATE
        elif request.url == 'https://localhost:5000/albuns/rate/' + str(id):
            albuns = query_db(
                "SELECT * FROM albuns WHERE id in(SELECT id_album FROM listas_albuns WHERE id_rate=?)", [int(id)])

            if len(albuns) > 0:
                delete = query_db(
                    "DELETE FROM albuns WHERE id in(SELECT id_album FROM listas_albuns WHERE id_rate=?)", [str(id)])
                r = make_response(json.dumps("removed!"))
                r.status_code = 200
            else:
                r = make_response(json.dumps("not found!"))
                r.status_code = 204
            return r

    # UPDATE
    elif request.method == 'PUT':

        if request.url == 'https://localhost:5000/albuns/' + str(id):
            data = json.loads(request.data)
            get_rate_id = query_db(
                "SELECT id FROM rates WHERE sigla=?", [data['rate']])

            if len(get_rate_id) > 0:
                update = query_db(
                    "UPDATE listas_albuns SET id_user=?, id_rate=? WHERE id_album = ?", [data['id_user'], get_rate_id[0], data['id_album']])
                r = make_response(
                    "UPDATE {} success!".format(data['id_album']))
                r.status_code = 200
            else:
                r = make_response("UPDATE {} failed!".format(data['id_album']))
                r.status_code = 204

            return r


if __name__ == '__main__':
    os.environ['DEBUG'] = "1"
    context = ("../certs/server.crt", "../certs/CA.key")
    app.secret_key = os.urandom(24)
    app.run(debug=True, ssl_context=context, threaded=True)
