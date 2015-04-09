import praw

# main function of isreactionary_bot by numandina
# this is a heavily edited version of the code for user_history_bot by mr_tato

class User:
    def __init__(self, username, r, suspicious_subs, score_thresh):
        self.r = r
        self.user = (self.r).get_redditor(username)
        self.username = username
        self.score_thresh = score_thresh
        self.suspicious_subs = suspicious_subs
        self.submitted = User_Post()
        self.comments = User_Post()

    ## Following are Getters ##
    def get_username(self):
        return self.username

    def get_submitted(self):
        return self.submitted

    def get_comments(self):
        return self.comments

    def get_number_of_comments(self):
        return (self.comments).get_count()

    def get_number_of_submitted(self):
        return (self.submitted).get_count()

    ## Following are Setters ##
    def set_submitted(self, new_submitted):
        self.submitted = new_submitted

    def set_commented(self, new_comments):
        self.commented = new_comments

    ## Insertion Methods ##
    def insert_comment(self, comment):
        (self.comments).insert(comment)

    def insert_submitted(self, submitted):
        (self.submitted).insert(submitted)

    def get_comments_by_subreddit(self, subreddit):
        return (self.comments).get_subreddit_posts(subreddit)

    def get_submitted_by_subreddit(self, subreddit):
        return (self.submitted).get_subreddit_posts(subreddit)

    # get all commenets from the user
    def process_comments(self):
        comment_iter = (self.user).get_comments(limit=None)
        for comment in comment_iter:
            (self.comments).insert(comment)

    # get all submissions from the user
    def process_submitted(self):
        submitted_iter = (self.user).get_submitted(limit=None)
        for submitted in submitted_iter:
            (self.submitted).insert(submitted)

    def get_monitoring_info(self):
        content = "/u/" + self.username + " post history contains participation in the following subreddits:\n\n"
        global_counter = 0
        post_condition = 0
        # first loop through user submissions
        post_dic = self.get_submitted().get_posts()
        for subreddit in sorted(post_dic, key=lambda k: len(post_dic[k]), reverse=True):
            num_posts = len(post_dic[subreddit])

            if subreddit.lower() in self.suspicious_subs:
                global_counter += 1
                tot_score = 0
                if num_posts > 1:
                    # get all submissions in detected subreddit
                    myposts = (self.submitted).get_subreddit_posts(subreddit)
                    post_no_n_link = ""

                    score = myposts[0].score

                    # loop through individual submissions in detected subreddit
                    for post_counter in range(1, len(myposts)):

                        # limit due to a limit in reddit comment character length
                         if post_counter < 8:
                             post_no_n_link += ", ["
                             post_no_n_link += "{}".format(post_counter + 1)
                             post_no_n_link += "]("
                             post_no_n_link += myposts[post_counter].permalink.replace("http://www.", "http://np.") + ")"
                         else:
                             post_no_n_link += ""
                         score += myposts[post_counter].score

                    post_no_n_link += ")"

                    if global_counter == 1:
                        content += "/r/" + subreddit + ": " + "{}".format(num_posts)
                        content += " posts ([1]("
                        content += myposts[0].permalink.replace("http://www.", "http://np.")
                        content += ")"
                        post_no_n_link + ", **combined score: " + "{}".format(score) + "**"
                    else:
                        content += ".\n\n/r/" + subreddit + ": "
                        content += "{}".format(num_posts) + " posts ([1]("
                        content += myposts[0].permalink.replace("http://www.", "http://np.")
                        content += ")" + post_no_n_link
                        content += ", **combined score: " + "{}".format(score) + "**"

                if num_posts == 1:
                    mypost = (self.submitted).get_subreddit_posts(subreddit)
                    score = mypost[0].score

                    if global_counter == 1:
                        content += "/r/" + subreddit + ": " + "{}".format(num_posts)
                        content += " post ([1]("
                        content += mypost[0].permalink.replace("http://www.", "http://np.")
                        content += ")), **combined score: " + "{}".format(score) + "**"
                    else:
                        content += ".\n\n/r/" + subreddit + ": " + "{}".format(num_posts)
                        content += " post ([1]("
                        content += mypost[0].permalink.replace("http://www.", "http://np.")
                        content += ")), **combined score: " + "{}".format(score) + "**"

                tot_score = score

                # get all user comments
                comment_dic = self.get_comments().get_posts()

                # check if user has comments in detected sub, if so add on the same line
                if subreddit in comment_dic:
                    num_comments = len(comment_dic[subreddit])

                    if num_comments > 1:
                        my_comments = (self.comments).get_subreddit_posts(subreddit)
                        score = my_comments[0].score
                        comment_no_n_link = ""

                        # loop through each of these comments
                        for comment_counter in range(1, len(my_comments)):
                            score += my_comments[comment_counter].score

                            permalink = "http://www.reddit.com/r/" + subreddit + "/comments/" + \
                            my_comments[comment_counter].link_id[3:] + "/_/" + my_comments[comment_counter].id

                            if comment_counter < 8:
                                comment_no_n_link += ", [" + "{}".format(comment_counter + 1) + "](" + \
                                permalink.replace("http://www.", "http://np.") + ")"
                            else:
                                comment_no_n_link += ""

                        comment_no_n_link += ")"

                        permalink = "http://www.reddit.com/r/" + subreddit + "/comments/" + \
                        my_comments[0].link_id[3:] + "/_/" + my_comments[0].id

                        content += "; " + "" + "{}".format(num_comments) + " comments ([1](" + \
                        permalink.replace("http://www.", "http://np.") + ")" + comment_no_n_link + \
                        ", **combined score: " + "{}".format(score) + "**"

                    if num_comments == 1:
                        my_comment = (self.comments).get_subreddit_posts(subreddit)
                        score = my_comment[0].score

                        permalink = "http://www.reddit.com/r/" + subreddit + "/comments/" + \
                        my_comment[0].link_id[3:] + "/_/" + my_comments[0].id

                        content += "; " + "" + "{}".format(num_posts2) + " comment ([1](" + \
                        permalink.replace("http://www.", "http://np.") + "))" + \
                        ", **combined score: " + "{}".format(score) + "**"

                    tot_score += score

                if tot_score > self.score_thresh:
                    post_condition += 1

        # we're done with subreddits, now go through comments
        comment_dic = self.get_comments().get_posts()

        for subreddit in sorted(comment_dic, key=lambda k: len(comment_dic[k]), reverse=True):
            num_comments = len(comment_dic[subreddit])

            if subreddit.lower() in self.suspicious_subs:
                global_counter += 1
                tot_score = 0

                # check if detected sub also has a post by the user. if it does then that means we already processed it
                post_dic2 = self.get_submitted().get_posts()
                if subreddit in post_dic2:
                    global_counter = global_counter
                else:
                    if num_comments > 1:
                        my_comments = (self.comments).get_subreddit_posts(subreddit)
                        score = my_comments[0].score
                        comment_no_n_link = ""

                        for comment_counter in range(1, len(my_comments)):
                            score += my_comments[comment_counter].score

                            permalink = "http://www.reddit.com/r/" + subreddit + "/comments/" + \
                            my_comments[comment_counter].link_id[3:] + "/_/" + my_comments[comment_counter].id

                            if comment_counter < 8:
                                comment_no_n_link += ", [" + "{}".format(comment_counter + 1) + "](" + \
                                permalink.replace("http://www.", "http://np.") + ")"
                            else:
                                comment_no_n_link += ""

                        comment_no_n_link += ")"

                        permalink = "http://www.reddit.com/r/" + subreddit + "/comments/" + \
                        my_comments[0].link_id[3:] + "/_/" + my_comments[0].id

                        if global_counter == 1:
                            content += "/r/" + subreddit + ": " + "{}".format(num_comments) + " comments ([1](" + \
                            permalink.replace("http://www.", "http://np.") + ")" + comment_no_n_link + \
                            ", **combined score: " + "{}".format(score) + "**"
                        else:
                            content += ".\n\n/r/" + subreddit + ": " + "{}".format(num_comments) + " comments ([1](" + \
                            permalink.replace("http://www.", "http://np.") + ")" + comment_no_n_link + \
                            ", **combined score: " + "{}".format(score) + "**"

                    if num_comments == 1:
                        my_comment = (self.comments).get_subreddit_posts(subreddit)
                        score = my_comment[0].score

                        permalink = "http://www.reddit.com/r/" + subreddit + "/comments/" + \
                        my_comment[0].link_id[3:] + "/_/" + my_comment[0].id

                        if global_counter == 1:
                            content += "/r/" + subreddit + ": " + "{}".format(num_comments) + " comment ([1](" + \
                            permalink.replace("http://www.", "http://np.") + "))" + \
                            ", **combined score: " + "{}".format(score) + "**"
                        else:
                            content += ".\n\n/r/" + subreddit + ": " + "{}".format(num_comments) + " comment ([1](" + \
                            permalink.replace("http://www.", "http://np.") + "))" + \
                            ", **combined score: " + "{}".format(score) + "**"

                    if tot_score > self.score_thresh:
                        post_condition += 1

        if global_counter > 0 and post_condition > 0:
            content += "."
        else:
            content = "User has not posted in monitored subreddits"

        return content

class User_Post:
    def __init__(self):
        self.post_dict = {}
        self.count = 0

    # This function takes a praw Comment object
    # and inserts it into the dictionary of comments,
    # comment_dict.
    def insert(self, post):
        subreddit = post.subreddit.display_name
        if subreddit not in self.post_dict:
                self.post_dict[subreddit] = []
        self.post_dict[subreddit].append(post)
        self.count += 1

    # This function returns the total number of comments
    def get_count(self):
        return self.count

    # Get the Post Dictionary
    def get_posts(self):
        return self.post_dict

    # This function takes a subreddit (str) and returns
    # a list of comments posted by the user. If subreddit
    # is not found, it returns None.
    def get_subreddit_posts(self, subreddit):
        if subreddit in self.post_dict:
            return self.post_dict[subreddit]
        return None
