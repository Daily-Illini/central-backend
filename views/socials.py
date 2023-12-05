from flask import (
    Blueprint,
    render_template,
    request
)
from flask_login import login_required
from datetime import datetime
from db.story import get_all_stories, add_story, delete_all_stories, check_limit
from util import restrict_to
import re

socials_routes = Blueprint('socials_routes', __name__, url_prefix='/socials')


@socials_routes.route('/dashboard')
@login_required
def dashboard():
    stories = get_all_stories()
    return render_template('socials.html', stories = stories)

@socials_routes.route('', methods=['GET'])
@login_required
def list_stories():
    return get_all_stories()

@socials_routes.route('/delete_all', methods=['POST'])
@login_required
@restrict_to(['webdev'])
def delete_all_story():
    delete_all_stories()
    return 'All stories deleted.'

@socials_routes.route('/illinoisapp', methods=['POST'])
@login_required
@restrict_to(['editors'])
def create_push_notification():
    if check_limit():
        return "ERROR: 3 push notifications have been sent in the past 7 days.", 200
    title = request.form['title']
    url = request.form['url']
    posted_to = "Illinois App"
    if (len(title) < 1):
        return "ERROR: Empty title.", 200
    if (len(url) < 1):
        return "ERROR: Empty URL.", 200
    if not is_valid_url(url):
        return "ERROR: Invalid URL.", 200
    add_story(title=title, url=url, posted_to=posted_to)
    return 'Illinois App push notification created.', 200

@socials_routes.route('/reddit', methods=['POST'])
@login_required
@restrict_to(['editors', 'di-section-editors', 'social'])
def create_reddit_post():
    title = request.form['title']
    url = request.form['url']
    posted_to = "Reddit"
    if (len(title) < 1):
        return "ERROR: Empty title.", 200
    if (len(url) < 1):
        return "ERROR: Empty URL.", 200
    if not is_valid_url(url):
        return "ERROR: Invalid URL.", 200
    add_story(title=title, url=url, posted_to=posted_to)
    return 'Reddit post created.', 200

def is_valid_url(url):
    url_pattern = re.compile(
        r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$',
        re.IGNORECASE
    )
    return bool(re.match(url_pattern, url))