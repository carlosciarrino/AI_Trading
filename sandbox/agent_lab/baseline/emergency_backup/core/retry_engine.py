import time


class RetryEngine:

    def __init__(self):

        self.max_retries = 3

        self.retry_delay = 2

    def execute_with_retry(self, func, event):

        attempts = 0

        while attempts < self.max_retries:

            try:

                func(event)

                print("[RETRY ENGINE] Success")

                return True

            except Exception as e:

                attempts += 1

                print(

                    f"[RETRY ENGINE] Attempt "
                    f"{attempts} failed: {e}"

                )

                time.sleep(self.retry_delay)

        return False
