import os
import shutil


class SelfRepair:

    def __init__(self):

        self.critical_files = [

            "mt4/ai_signal.txt",
            "data/trades/trades_log.txt"

        ]

    def check_critical_files(self):

        print("[SELF REPAIR] Checking critical files...\n")

        for file in self.critical_files:

            if not os.path.exists(file):

                print(f"[SELF REPAIR] Missing file: {file}")

                self.recreate_file(file)

    def recreate_file(self, filepath):

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w") as file:

            if "trades_log" in filepath:

                file.write(
                    "ticket,type,lot,open_price,close_price,profit,spread,score,result\n"
                )

            else:

                file.write("WAIT")

        print(f"[SELF REPAIR] Recreated: {filepath}")

    def quick_repair(self):

        for file in self.critical_files:

            if os.path.exists(file):

                if os.path.getsize(file) == 0:

                    print(f"[SELF REPAIR] Empty file repaired: {file}")

                    self.recreate_file(file)
