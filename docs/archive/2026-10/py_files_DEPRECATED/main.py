from core.orchestrator import Orchestrator


def main():

    system = Orchestrator()

    system.startup_check()

    system.main_loop()


if __name__ == "__main__":

    main()
