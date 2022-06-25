from app import App
import cProfile
from pstats import Stats


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    app = App()
    app.run()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(10)
