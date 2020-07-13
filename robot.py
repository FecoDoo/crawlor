# encoding=utf-8
import requests
import time
import json
import sys, os
import pandas as pd
from bs4 import BeautifulSoup as bf
from multiprocessing import Process, Lock
# from progress.bar import Bar

class MyRobot:
    def run(self):
        self.get_config()
        self.lock = Lock()
        self.get_content()
        # self.test_robot()

    def get_config(self):
        try:
            with open("config/robot.json", encoding="utf-8") as f:
                self.config = json.load(f)
            self.queue = pd.read_csv("data/queue.csv", usecols=["章节","url"]).values.tolist()
        
        except FileNotFoundError as e:
            print(e)

    def get_content(self):
        pool = []
        for i in range(self.config['number_of_process']):
            # bar = Bar(f"Robot {i}", max=self.config['capacity'])
            pool.append(
                Process(
                    target=self.robot,
                    args=(
                        i,
                        self.lock,
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
        process = Process(
                    target=self.robot,
                    args=(1, self.lock, self.queue[:20])
                )
        process.start()
        process.join()
    
    def robot(self, mark, lock, data=[]):
        
            lost = []
            for i in range(len(data)):
                try:
                    page = requests.get(
                        url=self.config["url"] + data[i][1], headers=self.config["headers"],
                        timeout=20
                    )
                    if page:
                        page.encoding = self.config["encoding"]
                        soup = bf(page.text, "lxml")
                        content = soup.select(self.config["selector"])
                        
                        res = "".join(content[0].get_text().split())
                        # # res = res.replace(self.config["replacement"], "")
                        with open(
                            f"book/{self.config['book']}/{mark}.txt",
                            "a",
                            encoding="utf-8",
                        ) as f:
                            f.writelines(["\n\n", data[i][0], "\n", res])
                        # bar.next()
                        if (i % 25) == 0:
                            print(f"Process {mark} reached: {i}")
                    else:
                        lost.append(i)
                
                except Exception as e:
                    print(f"Process {mark} error: {e}")
                    continue
                
            # 添加失败页
            try:
                if not lost:
                    data = {mark: lost}
                    with lock:
                        with open(f"book/{self.config['book']}/lost.txt", 'a') as f:
                            json.dump(data, f)

            except Exception as e:
                print(f"Process {mark} error: {e}")
                return

            finally:
                print(f"Process {mark} complete!")
            
        
        


if __name__ == "__main__":
    robot = MyRobot()
    robot.run()
