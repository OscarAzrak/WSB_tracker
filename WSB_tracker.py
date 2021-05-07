from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import re
api = PushshiftAPI()

start_time = int(dt.datetime(2021,4,28).timestamp())

submissions = (api.search_submissions(after=start_time,
                                            subreddit= 'wallstreetbets',
                                            filter=['url','author', 'title', 'subreddit']
                                      ))


stocks = []
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

df = []
for submissions in submissions:
    #print(submissions)
    content = {
        "title": submissions.title
    }
    #print(content)
    df.append(content)
df = pd.DataFrame(df)

regex = re.compile('[^a-zA-Z ]')
word_dict = {}
for (index, row) in df.iterrows():
  title = row['title']
  title = regex.sub('', title)
  title_words = title.split(' ')
  words = title_words
  for x in words:
    if x in ['A', 'B', 'C', 'D', 'E', 'G', 'M', 'GO', 'ARE', 'ON', 'IT', 'ALL', 'NEXT', 'PUMP', 'AT', 'NOW', 'FOR', 'TD', 'CEO', 'AM', 'K', 'BIG', 'BY', 'LOVE', 'CAN', 'BE', 'SO', 'OUT', 'STAY', 'OR', 'NEW', 'RH', 'EDIT', 'ONE', 'ANY', 'DD']:
      pass
    elif x in word_dict:
      word_dict[x] += 1
    else:
      word_dict[x] = 1

word_df = pd.DataFrame.from_dict(list(word_dict.items())).rename(columns={0: "Term", 1: "Mentions"})

ticker_df = pd.read_csv('tickers.csv').rename(columns={'Symbol':'Term', 'Name':'Company_Name'})
stonks_df = pd.merge(ticker_df, word_df, on='Term')
stonks_df = stonks_df.sort_values(by="Mentions", ascending=False, ignore_index=True).head(20)


print(stonks_df)


