# encoding=utf-8
import requests
import time
import json
import sys, os
import pandas as pd
from bs4 import BeautifulSoup as bf
from multiprocessing import Process
from progress.bar import Bar

class MyRobot:
    def run(self):
        self.get_config()
        self.get_content()
        # self.test_robot()

    def get_config(self):
        try:
            with open("小说/robot.json", encoding="utf-8") as f:
                self.config = json.load(f)
            self.queue = pd.read_csv("小说/queue.csv", usecols=["章节","url"]).values.tolist()
        
        except FileNotFoundError as e:
            print(e)

    def get_content(self):
        pool = []
        for i in range(self.config['number_of_process']):
            bar = Bar(f"Robot {i}", max=self.config['capacity'])
            pool.append(
                Process(
                    target=self.robot,
                    args=(
                        i,
                        bar,
                        self.queue[
                            i
                            * self.config["capacity"] : (i + 1)
                            * self.config["capacity"]
                        ],
                    ),
                )
            )

        for i in range(self.config['number_of_process']):
            pool[i].start()

        for i in range(self.config['number_of_process']):
            pool[i].join()

    def test_robot(self):
        print(self.queue[:2])
        process = Process(
                    target=self.robot,
                    args=(1,self.queue[:2],)
                )
        process.start()
        process.join()
    
    def robot(self, mark, bar, data=[]):
        
        for i in range(len(data)):
            page = requests.get(
                url=self.config["url"] + data[i][1], headers=self.config["headers"]
            )
            page.encoding = self.config["encoding"]
            soup = bf(page.text, "lxml")
            content = soup.select(self.config["selector"])
            
            res = "".join(content[0].get_text().split())
            # # res = res.replace(self.config["replacement"], "")
            with open(
                f"{self.config['path'] + self.config['book']}-{mark}.txt",
                "a",
                encoding="utf-8",
            ) as f:
                f.writelines(["\n\n", data[i][0], "\n", res])
            bar.next()
            time.sleep(0.2)


if __name__ == "__main__":
    robot = MyRobot()
    robot.run()
