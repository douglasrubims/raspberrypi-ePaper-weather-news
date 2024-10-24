# -*- coding:utf-8 -*-

import requests
import textwrap

class News:
  def __init__(self):
    pass

  def update(self, api_id):
    print("Getting news from NewsAPI.org")
    print(f"https://newsapi.org/v2/top-headlines?sources=google-news-br&apiKey={api_id}")
    self.news_list = requests.get(
      f"https://newsapi.org/v2/top-headlines?sources=google-news-br&apiKey={api_id}").json()
    print("News received from NewsAPI.org")
    return self.news_list

  def selected_title(self):
    list_news = []
    if self.news_list["status"] == "ok":
      for i in range(len(self.news_list["articles"])):
        line = "> " + self.news_list["articles"][i]["title"]
        line = textwrap.wrap(line, width=58)
        list_news.append(line)
    else:
      list_news = ["Erro ao carregar as notícias"]
    return list_news
