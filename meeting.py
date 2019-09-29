from settings import settings
from surveymonkey import surveymonkey

config = settings.Settings()


def main():
    print(dir(config))
    print(config)


main()
