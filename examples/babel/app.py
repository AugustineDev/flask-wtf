from flask import Flask, render_template, request
from flask.ext.wtf import Form, TextField, Required
from flask.ext.babel import Babel
from flask.ext.babel import lazy_gettext as _


class BabelForm(Form):
    name = TextField(_('Name'), validators=[Required()])


DEBUG = True
SECRET_KEY = 'secret'
WTF_I18N_ENABLED = True

app = Flask(__name__)
app.config.from_object(__name__)

# config babel
babel = Babel(app)


@babel.localeselector
def get_locale():
    """how to get the locale is defined by you.

    Match by the Accept Language header::

        match = app.config.get('BABEL_SUPPORTED_LOCALES', ['en', 'zh'])
        default = app.config.get('BABEL_DEFAULT_LOCALES', 'en')
        return request.accept_languages.best_match(match, default)
    """
    # this is a demo case, we use url to get locale
    code = request.args.get('lang', 'en')
    return code


@app.route("/", methods=("GET", "POST",))
def index():
    form = BabelForm()
    if form.validate_on_submit():
        pass
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run()
