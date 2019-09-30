from settings import settings
from surveymonkey import surveymonkey

config = settings.Settings()


def main():
    print(config.meetup_weekday)
    print(config.survey_weekday)


main()
