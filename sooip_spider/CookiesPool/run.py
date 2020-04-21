import sys
sys.path.append('..')
from cookiespool.scheduler import Scheduler


def main():
    s = Scheduler()
    s.run()


if __name__ == '__main__':
    main()
