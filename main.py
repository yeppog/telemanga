from app import App
import cProfile, os
from pstats import Stats


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    try:
        os.makedirs('output')
    except OSError as e:
        print(e)

    app = App()
    app.run()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(10)
