from __future__ import with_statement

from speaklater import _LazyString
from flask.json import JSONEncoder
from flask import Flask, render_template, jsonify
from flask.ext.wtf import Form, TextField, HiddenField, SubmitField, Required


def to_unicode(text):
    return text.decode('utf-8')


class _JSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, _LazyString):
            return str(o)
        return JSONEncoder.default(self, o)


class MyForm(Form):
    SECRET_KEY = "a poorly kept secret."
    name = TextField("Name", validators=[Required()])
    submit = SubmitField("Submit")


class HiddenFieldsForm(Form):
    SECRET_KEY = "a poorly kept secret."
    name = HiddenField()
    url = HiddenField()
    method = HiddenField()
    secret = HiddenField()
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(HiddenFieldsForm, self).__init__(*args, **kwargs)
        self.method.name = '_method'


class SimpleForm(Form):
    SECRET_KEY = "a poorly kept secret."
    pass


class TestCase(object):
    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def create_app(self):
        app = Flask(__name__)
        app.json_encoder = _JSONEncoder
        app.secret_key = "secret"

        @app.route("/", methods=("GET", "POST"))
        def index():

            form = MyForm()
            if form.validate_on_submit():
                name = form.name.data.upper()
            else:
                name = ''

            return render_template("index.html",
                                   form=form,
                                   name=name)

        @app.route("/simple/", methods=("POST",))
        def simple():
            form = SimpleForm()
            form.validate()
            assert form.csrf_enabled
            assert not form.validate()
            return "OK"

        @app.route("/two_forms/", methods=("POST",))
        def two_forms():
            form = SimpleForm()
            assert form.csrf_enabled
            assert form.validate()
            assert form.validate()
            form2 = SimpleForm()
            assert form2.csrf_enabled
            assert form2.validate()
            return "OK"

        @app.route("/hidden/")
        def hidden():

            form = HiddenFieldsForm()
            return render_template("hidden.html", form=form)

        @app.route("/ajax/", methods=("POST",))
        def ajax_submit():
            form = MyForm()
            if form.validate_on_submit():
                return jsonify(name=form.name.data,
                               success=True,
                               errors=None)

            return jsonify(name=None,
                           errors=form.errors,
                           success=False)

        return app
