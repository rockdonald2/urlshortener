from flask import redirect, url_for, render_template, flash, abort
from shorturl import app, cache, WEBSITE_DOMAIN, API_URL
from shorturl.form import URLForm
from shorturl.slug import gen_slug
from requests import get, post
from datetime import datetime, timedelta
from json import dumps

""" 
TODO: don't let people upload duplicate links - SOLVED
* Duplication is an interesting topic, because we work with URLs
* Duplicated URL is a URL which path is identical with an existing one in the database.
* For this, we will only store the path in the database, removing any scheme, or www parts.
TODO: expiration time for existing slugs - SOLVED
* To have this we have to create a TTL index, in order to let mongoDB remove for us documents that are expired
* We will remove documents that are older than 1 week
* Because the RESTful API module we use Python Eve, doesn't support indexes, we have to do this manually,
* within the command-line.
* $ db.storage.createIndex( { “expireAt”: 1 }, { expireAfterSeconds: 0 } )
* After this, all of our entries have to have an expireAt item.
TODO: cache - SOLVED
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()

    if form.validate_on_submit():
        # * we make the path, the barebone version of the provided URL
        path = form.url.data
        if path.startswith('http://'):
            path = path[7:]
        elif path.startswith('https://'):
            path = path[8:]
        if path.startswith('www.'):
            path = path[4:]

        check = get(API_URL + 'storage?where={"url":"' + path + '"}').json()['_items']

        if check:
            flash('This path was already in our database')
            return render_template('slug.html', title='Short URL', url=WEBSITE_DOMAIN + '/' + check[0]['slug'])

        # * we generate the unique slog that appears after the WEBSITE_DOMAIN
        slug = gen_slug()

        entry = {
            'slug': slug,
            'url': path,
            'expireAt': (datetime.today() + timedelta(days=7)).isoformat()
        }

        headers = {
            'Content-Type': 'application/json'
        }

        # * after we got the slug, we make a POST request to the database, uploading our new entry
        resp = post(API_URL + 'storage/', dumps(entry), headers=headers)

        """ flash('Validated submitted url: {}, with slug: {}'.format(path, slug)) """
        return render_template('slug.html', title='Short URL', url='http://' + WEBSITE_DOMAIN + '/' + slug)

    return render_template('index.html', title='URL Shortener', form=form)


@app.route('/<slug>', methods=['GET'])
@cache.cached(timeout=600)
def redirect_url(slug):
    check = get(API_URL + 'storage?where={"slug":"' + slug + '"}').json()['_items']

    if not check:
        abort(404, 'URL not found in our system')

    return redirect('http://' + check[0]['url'])
    

@app.errorhandler(404)
@app.errorhandler(422)
@app.errorhandler(500)
@app.errorhandler(401)
@app.errorhandler(405)
@app.errorhandler(403)
def error_handler(e):
    return render_template('error.html', title='Error - Something went wrong', error=str(e))