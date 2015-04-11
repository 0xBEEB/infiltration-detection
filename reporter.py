try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


class UserReport:

    def __init__(self, user, suspicious_subs):
        self.first = True
        self.user = user
        self.suspicious_subs = suspicious_subs
        self.outString = None

    def __str__(self):
        return self.write()

    def write(self):
        if self.outString == None:
            self.output = StringIO()
            self._process_data()
            self.outString = self.output.getvalue()
            self.output.close()
        return self.outString

    def _process_data(self):
        data = {}
        post_dic = self.user.get_submitted().get_posts()
        comment_dic = self.user.get_comments().get_posts()

        for subreddit in sorted(post_dic, key=lambda k: len(post_dic[k]), reverse=True):
            if subreddit.lower() in self.suspicious_subs:
                if subreddit.lower() not in data:
                    data[subreddit.lower()] = {}
                data[subreddit.lower()]['posts'] = self.user.submitted.get_subreddit_posts(subreddit)


        for subreddit in sorted(comment_dic, key=lambda k: len(comment_dic[k]), reverse=True):
            if subreddit.lower() in self.suspicious_subs:
                if subreddit.lower() not in data:
                    data[subreddit.lower()] = {}
                data[subreddit.lower()]['comments'] = self.user.comments.get_subreddit_posts(subreddit)

        if len(data.keys()) < 1:
            self.output.write("User has not posted in monitored subreddits")
            return
        else:
            self.output.write("/u/%s " % self.user.username)
            self.output.write("post history contains participation in the ")
            self.output.write("following subreddits:\n\n")
            for subreddit in sorted(data, key=lambda k: ((0 if 'posts' not in data[k] else len(data[k]['posts'])), (0 if 'comments' not in data[k] else len(data[k]['comments']))), reverse=True):
                self._write_data(subreddit, data[subreddit])
            self.output.write(".")


    def _write_data(self, subreddit, sub_data):
        prefix = ""

        if self.first:
            self.first = False
        else:
            prefix = ".\n\n"

        self.output.write("%s/r/%s: " % (prefix, subreddit))

        if 'posts' in sub_data:
            self._write_post_data(sub_data['posts'])
        if 'comments' in sub_data:
            if 'posts' in sub_data:
                self.output.write("; ");
            self._write_comment_data(subreddit, sub_data['comments'])

    def _write_post_data(self, posts):

        if len(posts) < 1:
            return
        elif len(posts) == 1:
            score = posts[0].score
            link = posts[0].permalink
            link = link.replace("http://www.", "http://np.")
            self.output.write("%d post ([1](%s)), **total score: %d;**" % (len(posts), link, score))
        elif len(posts) > 1:
            score = 0
            self.output.write("%d posts (" % (len(posts)))

            for post_counter in range(0, len(posts)):
                prefix = "" if post_counter == 0 else  ", "
                # limit due to a limit in reddit comment character length
                if post_counter < 8:
                    link = posts[post_counter].permalink
                    link = link.replace("http://www.", "http://np.")
                    self.output.write("%s[%d](%s)" % (prefix, post_counter + 1, link))
                score += posts[post_counter].score

            self.output.write("), **total score: %d**" % (score))


    def _write_comment_data(self, subreddit, comments):

        if len(comments) < 1:
          return
        elif len(comments) == 1:
            score = comments[0].score
            permalink = "http://www.reddit.com/r/%s/comments/%s/_/%s" % (subreddit, comments[0].link_id[3:], comments[0].id)
            link = permalink.replace("http://www.", "http://np.")
            self.output.write("%d comment ([1](%s))" % (len(comments), link))
            self.output.write(", **total score: %d**" % score);
        elif len(comments) > 1:
            score = 0
            self.output.write("%d comments (" % len(comments))

            # loop through each of these comments
            for comment_counter in range(0, len(comments)):
                score += comments[comment_counter].score
                permalink = "http://www.reddit.com/r/%s/comments/%s/_/%s" % (subreddit, comments[comment_counter].link_id[3:], comments[comment_counter].id)
                link = permalink.replace("http://www.", "http://np.")
                prefix = "" if comment_counter == 0 else ", "

                if comment_counter < 8:
                    self.output.write("%s[%d](%s)" % (prefix, comment_counter + 1, link))

            self.output.write("), **combined score: %d**" % score)
