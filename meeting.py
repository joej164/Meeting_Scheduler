from settings import settings
from surveymonkey import surveymonkey

config = settings.Settings()





def main():
    user_data = prompt_user_for_info()
    print(user_data)


main()
