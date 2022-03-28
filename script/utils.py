import feedparser

def read_rss_link(url):
    feeds = []
    NewsFeed = feedparser.parse(url)

    for feed in NewsFeed.entries:
        feed_json = {}
        feed_json['title'] = feed.title
        feed_json['link'] = feed.link
        feed_json['short'] = feed.id
        feed_json['published'] = feed.published
        feeds.insert(feed_json)

    return feeds