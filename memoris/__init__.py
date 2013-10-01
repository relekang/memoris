from flask import Flask

from views import index, api

app = Flask(__name__)

app.add_url_rule('/', view_func=index)
app.add_url_rule('/<key>', view_func=api)

if __name__ == '__main__':
    app.run()
