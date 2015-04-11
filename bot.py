#!/usr/bin/env python
import time
import sys
import HTMLParser
import praw
from models import User
from reporter import UserReport
from config import settings


class Bot:

    def __init__(self, username, password):
        self.reddit = praw.Reddit('PRAW infiltration detection by /u/flaxrabbit v 1.0. ' +
                        'Url: http://github.com/ubiquill/infiltration-detection')
        self.reddit.login(username, password)
        self.update_from_wiki()

    def update_from_wiki(self):
        try:
            subreddit = self.reddit.get_subreddit(settings['subreddit'])
            page = subreddit.get_wiki_page(settings['wiki_page_name'])
        except Exception:
            return False

        html_parser = HTMLParser.HTMLParser()
        page_content = html_parser.unescape(page.content_md)

        self.suspicious_subs = page_content.split()

    def check_and_respond(self):
        new_messages = self.reddit.get_unread(limit=None)

        for msg in new_messages:
            msg.mark_as_read()
            user_to_infiltrate = self.get_user_name_from_message(msg.body)
            user = User(user_to_infiltrate, self.reddit)

            report = UserReport(user, self.suspicious_subs)
            info = report.write()

            if len(info) > 0:
                info += "\n\n___\n\n^I'm ^a ^bot. ^Only ^the ^past ^1,000 ^comments ^are ^fetched."
                info.replace("http://www.", "http://np.")
                info = info[:10000]

            msg.reply(info)

    def get_user_name_from_message(self, body):
        possible_users = [user for user in body.split() if user.startswith('/u/')]
        if len(possible_users) > 0:
            return possible_users[0][3:]
        possible_users = [user for user in body.split() if user.startswith('u/')]
        if len(possible_users) > 0:
            return possible_users[0][2:]
        possible_users = body.split()
        if len(possible_users) > 0:
            return possible_users[0]


def main():
    count = 0
    bot = Bot(settings['username'], settings['password'])

    while True:
        try:
            time.sleep(settings['delay'])
            bot.check_and_respond()
            if count == 5:
                bot.update_from_wiki()
                count = 0
            else:
                count += 1
        except KeyboardInterrupt:
            print "Exiting\n"
            sys.exit(0)
        except:
            pass

if __name__ == "__main__":
    main()
