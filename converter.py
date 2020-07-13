import json


class Converter:
    def run(self):
        config = None
        with open("config/robot.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        for i in range(config["number_of_process"]):
            with open(f"book/{config['book']}/{i}.txt", "r", encoding="utf-8") as f:
                chapter = f.readlines()
                with open(
                    f"book/{config['book']}/{config['book']}.txt", "a", encoding="utf-8"
                ) as b:
                    b.writelines(chapter)
