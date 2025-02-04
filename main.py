import os
import json
import random
import time
from checks.checker import Checker
from checks.models.check import Check
from checks.models.rule_website import RuleWebsite


CONFIG_PATH = 'config.json'
ARCHIVE_PATH = 'archive'
checker = Checker()

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Check) or isinstance(obj, RuleWebsite):
            return obj.to_dict()
        return super().default(obj)

class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if obj.get('class') == 'Check':
            return Check.from_dict(obj)
        elif obj.get('class') == 'RuleWebsite':
            return RuleWebsite.from_dict(obj)
        return obj

def init():
    if not os.path.exists(CONFIG_PATH):
        json_data = []
        sample_check = Check()
        sample_check.name = "MSI GeForce RTX 5090 Ventus 3X OC"
        sample_check.add_rule(
            RuleWebsite(
                "Alternate DE",
                "https://www.alternate.de/MSI/GeForce-RTX-5090-32G-VENTUS-3X-OC-Grafikkarte/html/product/100109567",
                "In den Warenkorb",
                ".cart-btn-text"
            )
        )
        sample_check.add_rule(
            RuleWebsite(
                "Amazon DE",
                "https://www.amazon.de/dp/B0DT6S77JK",
                "Auf Lager",
                "#availability"
            )
        )
        json_data.append(sample_check)

        with open(CONFIG_PATH, 'w', encoding='utf-8') as config_file:
            json.dump(json_data, config_file, indent=4, cls=CustomJSONEncoder)

        print(f"Config file not found, created sample config: \033[91m{CONFIG_PATH}\033[0m")
        print("\033[91mPlease edit the config file and restart the program.\033[0m")
        exit(0)

    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file, cls=CustomJSONDecoder)
        for check in config:
            if isinstance(check, Check):
                checker.add_check(check)

    if os.path.exists(ARCHIVE_PATH):
        for file in os.listdir(ARCHIVE_PATH):
            file_path = os.path.join(ARCHIVE_PATH, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(ARCHIVE_PATH, exist_ok=True)

def main_loop():
    checker.print_status()
    while True:
        checker.run()
        wait_time = random.randint(10, 30)
        print(f"\n\nNext check in {wait_time} seconds...")
        time.sleep(wait_time)

if __name__ == '__main__':
    init()
    main_loop()