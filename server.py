from flask import Flask, redirect, request, render_template, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)

# This option will cause Jinja to throw UndefinedErrors if a value hasn't
# been defined (so it more closely mimics Python's behavior)
app.jinja_env.undefined = StrictUndefined

# This option will cause Jinja to automatically reload templates if they've been
# changed. This is a resource-intensive operation though, so it should only be
# set while debugging.
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'ABC'

MOST_LOVED_MELONS = {
    'cren': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimRegular/crenshaw.jpg',
        'name': 'Crenshaw',
        'num_loves': 584,
    },
    'jubi': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Jubilee-Watermelon-web.jpg',
        'name': 'Jubilee Watermelon',
        'num_loves': 601,
    },
    'sugb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Sugar-Baby-Watermelon-web.jpg',
        'name': 'Sugar Baby Watermelon',
        'num_loves': 587,
    },
    'texb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Texas-Golden-2-Watermelon-web.jpg',
        'name': 'Texas Golden Watermelon',
        'num_loves': 598,
    },
}

melon_list = list(MOST_LOVED_MELONS.values())



@app.route("/")
def homepage():
    return render_template("homepage.html")



@app.route('/get-name', methods=["POST"])
def get_name():

    user = request.form.get('nm')

    if user:
        session['user'] = user
        return redirect('/top-melons')
    else:
        return redirect('/')
    


@app.route("/top-melons")
def list_loved_melons():

    print(melon_list)

    if "user" in session: 
        user = session["user"]
        return render_template("top-melons.html", melon_list=melon_list, user=user)
    else:
        return render_template("homepage.html")


@app.route('/love-melon', methods=["POST"])
def get_melon():
    
    melon = request.form.get('melon')
    MOST_LOVED_MELONS[melon]['num_loves'] += 1
    return render_template("thank-you.html", user=user)



if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
