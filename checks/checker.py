import os
from checks.models.check import Check

class Checker:
    def __init__(self):
        self._checks = []

    def send_notification(self, message: str):
        if not message:
            return

        from plyer import notification
        notification.notify(
            title="NOW AVAILABLE!",
            message=message,
            app_name="StockChecker",
            timeout=10
        )

        from playsound3 import playsound
        playsound("notification.mp3")

    def add_check(self, check: Check):
        self.checks.append(check)

    def run(self):
        for check in self.checks:
            self.print_status(check.name)
            check.check(self)
            self.print_status()
            if check.last_status is not None and check.last_status != check.status and check.status == check.IN_STOCK:
                self.send_notification(check.name)

    def print_status(self, highlight_name: str = None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * (3 + 30 + 30 + 20 + 20))
        print(f"{'Name':<30} {'Last Check':<30} {'Previous Status':<20} {'Current Status':<20}")
        for check in self.checks:
            print("-" * (3 + 30 + 30 + 20 + 20))
            if highlight_name and check.name == highlight_name:
                print("\033[1m", end="")
            if check.last_status != "None" and check.last_status != check.status:
                print(
                    f"{check.name[:28]:<30} {check.last_run[:28]:<30} {check.last_status[:18]:<20} \033[91m{check.status[:18]:<20}\033[0m"
                )
            else:
                print(
                    f"{check.name[:28]:<30} {check.last_run[:28]:<30} {check.last_status[:18]:<20} {check.status[:18]:<20}"
                )
            for rule in check.rules:
                if rule.last_status != "None" and rule.last_status != rule.status:
                    print(
                        f"  - {rule.name[:24]:<26} {rule.last_run[:28]:<30} {rule.last_status[:18]:<20} \033[91m{rule.status[:18]:<20}\033[0m"
                    )
                else:
                    print(
                        f"  - {rule.name[:24]:<26} {rule.last_run[:28]:<30} {rule.last_status[:18]:<20} {rule.status[:18]:<20}"
                    )
                if rule.status == rule.IN_STOCK and rule.information:
                    print(f"    \033[92m{rule.information}\033[0m")
            if highlight_name and check.name == highlight_name:
                print("\033[0m", end="")
        print("=" * (3 + 30 + 30 + 20 + 20))

    @property
    def checks(self):
        return self._checks