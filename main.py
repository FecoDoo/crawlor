import requests
import json
from bs4 import BeautifulSoup as bf
import pandas as pd
from robot import MyRobot
import os


class getUrl:
    def run(self):
        self.get_config()
        self.get_url()

    def get_config(self):
        try:
            with open("config/config.json", encoding="utf-8") as f:
                self.config = json.load(f)
            os.mkdir(f"book/{self.config['book']}")
        except FileNotFoundError as e:
            print(e)

    def get_url(self):
        page = requests.get(
            url=self.config["url"] + self.config["catalog"],
            headers=self.config["headers"],
        )
        page.encoding = self.config["encoding"]
        soup = bf(page.text, "lxml")
        content = soup.select(self.config["selector"])

        data = []
        for i in content:
            data.append([i.string, i.get("href")])

        pd.DataFrame(data, columns = ["章节","url"]).to_csv("data/queue.csv")
        
        self.queue_length = len(data)
        self.number_of_process = self.queue_length // self.config['capacity']
        
        cf = {
            "book": self.config['book'],
            "url": self.config['url'],
            "headers": self.config['headers'],
            "capacity": self.config['capacity'],
            "encoding": self.config['encoding'],
            "selector": self.config['content_selector'],
            "queue_length": self.queue_length,
            "number_of_process": self.number_of_process
        }

        with open('config/robot.json', 'w', encoding='utf-8') as f:
            json.dump(cf, f)

if __name__ == "__main__":
    get = getUrl()
    get.run()

    robot = MyRobot()
    robot.run()