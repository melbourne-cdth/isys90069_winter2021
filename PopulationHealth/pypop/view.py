import itables
from IPython.display import display, HTML
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
import ipywidgets as ipw
import json

def show_data(df):
    return itables.show(df, maxBytes=0)

def _format_json(data):
    """Pretty print a dict as a JSON, with colors if pygments is present."""
    output = json.dumps(data, indent=4, sort_keys=True)

    return highlight(output, JsonLexer(), HtmlFormatter(style='colorful'))

def view_tweet(tweet):

    display(HTML(_format_json(tweet)))

def view_tweet_n(data, n):
    view_tweet(data[n])


def view_random_tweet(data):
    tweet = random.choice(data)
    view_tweet(tweet)
