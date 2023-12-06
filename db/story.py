import uuid
from datetime import datetime, timedelta
from google.cloud import ndb

from . import client


class Story(ndb.Model):
    id = ndb.StringProperty()
    title = ndb.StringProperty()
    url = ndb.StringProperty()
    posted_to = ndb.StringProperty()
    posted_at = ndb.DateTimeProperty()


def add_story(title, url, posted_to):
    with client.context():
        # Story's id is auto generated by using uuid.uuid1() when posting a story
        # posted_at will get the current time
        story = Story(id=str(uuid.uuid1()), title=title, url=url, posted_to=posted_to, posted_at=datetime.now())
        story.put()
    return story


def get_all_stories():
    with client.context():
        stories = [story.to_dict() for story in Story.query().fetch()]
    return stories


def get_recent_stories(count):
    with client.context():
        stories = [story.to_dict() for story in Story.query().order(-Story.posted_at).fetch(limit=count)]
    return stories


def delete_all_stories():
    with client.context():
        stories = Story.query().fetch()
        for story in stories:
            story.key.delete()
    return stories


def get_story(id):
    if id is None:
        return None
    with client.context():
        story = Story.query().filter(Story.id == id).get()
    if story is None:
        return None
    return story


def check_limit():
    with client.context():
        current_datetime = datetime.now()
        seven_days_ago = current_datetime - timedelta(days=7)
        recent_stories = Story.query().filter(
            Story.posted_to == "Illinois App",
            Story.posted_at >= seven_days_ago,
            Story.posted_at <= current_datetime
        ).fetch()
    return len(recent_stories) >= 3