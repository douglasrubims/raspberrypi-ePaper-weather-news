# -*- coding:utf-8 -*-

import requests
import textwrap

class News:
  def __init__(self):
    pass

  def update(self, api_id):
    print("Getting news from NewsData.io")
    print(f"https://newsdata.io/api/1/latest?apikey={api_id}&country=br&size=5")
    self.news_list = requests.get(
      f"https://newsdata.io/api/1/latest?apikey={api_id}&country=br&size=5").json()
    print("News received from NewsData.io")
    print(self.news_list)
    return self.news_list

  def selected_title(self):
    list_news = []
    if self.news_list["status"] == "success":
      for i in range(len(self.news_list["results"])):
        line = "> " + self.news_list["results"][i]["title"]
        line = textwrap.wrap(line, width=58)
        list_news.append(line)
    else:
      list_news = ["Erro ao carregar as notícias"]
    return list_news
