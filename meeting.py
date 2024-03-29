from settings import settings
from surveymonkey import surveymonkey


def main():
    config = settings.Settings()
    survey = surveymonkey.Surveymonkey(config)
    r = survey.create_new_survey()
    print(r)

    s = survey.get_survey_details()
    print(s)

    t = survey.update_survey_page()
    print(t)

    print(config.survey_href)
    print(config.pages_href)
    u = survey.add_survey_questions()
    print(u)

    v = survey.create_collector()
    print(v)
    print()
    print(f'The survey url is: {v["url"]}')


main()
