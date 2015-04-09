#!/usr/bin/env python
import time
import praw
import sys
from models import User
from config import settings


class Bot:

    def __init__(self, username, password, subs):
        self.reddit = praw.Reddit('PRAW infiltration detection by /u/flaxrabbit v 1.0. ' +
                        'Url: http://github.com/ubiquill/infiltration-detection')
        self.reddit.login(settings['username'], settings['password'])

        suspicious_subs = settings['suspicious_subs']

    def check_and_respond(self):
        new_messages = r.get_unread(limit=None)

        for msg in new_messages:
            msg.mark_as_read()
            user_to_infiltrate = get_user_name_from_message(msg.body)
            user = User(user_to_infiltrate, r, suspicious_subs, 50)
            user.process_comments()
            user.process_submitted()

            info = user.get_monitoring_info()

            if len(info) > 0:
                info += "\n\n___\n\n^I'm ^a ^bot. ^Only ^the ^past ^1,000 ^comments ^are ^fetched."
                info.replace("http://www.", "http://np.")
                info = info[:10000]
            msg.reply(info)


    def get_user_name_from_message(body):
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
    bot = Bot(settings['username'],
              settings['password'],
              settings['suspicious_subs'])

    try:
        bot.check_and_respond()
    except KeyboardInterrupt:
        print "Exiting\n"
        sys.exit(0)
    except:
        pass

if __name__ == "__main__":
    main()