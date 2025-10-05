import praw
import pandas as pd
import time, os

reddit = praw.Reddit(
    client_id="ZP4GZf5XfJl2TWflwMPCgA",
    client_secret="ToL2yc94rlJuyFHtIthffw5UkNsKLg",
    user_agent="BigData by minmin_90"
)

queries = ["work life balance", "burnout", "mental health", "stress", "overwork"]
subreddits = ["WorkLifeBalance", "antiwork", "productivity", "GetDisciplined", "selfimprovement"]

posts, comments = [], []

for sub in subreddits:
    for q in queries:
        print(f"Scraping r/{sub} - query: {q}")
        for submission in reddit.subreddit(sub).search(q, limit=1000, sort="new"):
            posts.append({
                "id": submission.id,
                "subreddit": sub,
                "query": q,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "num_comments": submission.num_comments,
                "created_utc": submission.created_utc,
                "url": submission.url
            })

            submission.comments.replace_more(limit=0)
            for comment in submission.comments[:20]:
                comments.append({
                    "post_id": submission.id,
                    "body": comment.body,
                    "score": comment.score,
                    "created_utc": comment.created_utc
                })
            time.sleep(1)

os.makedirs("../data/raw", exist_ok=True)
pd.DataFrame(posts).to_csv("../data/raw/reddit_posts.csv", index=False)
pd.DataFrame(comments).to_csv("../data/raw/reddit_comments.csv", index=False)
print(f"Crawling selesai. {len(posts)} post & {len(comments)} komentar disimpan.")
