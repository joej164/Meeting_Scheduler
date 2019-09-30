# Functions and files to work with Survey Monkey
import requests


class SurveyMonkeyError(Exception):
    pass


class Surveymonkey():
    def __init__(self, config):
        self.config = config
        self.config.survey_id = None
        self.config.survey_href = None
        self.config.pages_href = None
        self.config.pages_id = None

    def create_new_survey(self):
        payload = {"title": f"{self.config.survey_title}"}

        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {self.config.token}"
        }
        method = "surveys"
        print(self.config)
        print(type(self.config))
        url = self.config.survey_api_url + method

        response = requests.request("POST", url, json=payload, headers=headers)

        if not response.ok or response.status_code in [400, 404]:
            print(url)
            print(response.text)
            raise SurveyMonkeyError("The Survey Monkey API did not respond properly")

        try:
            r = response.json()
            self.config.survey_id = r['id']
            self.config.survey_href = r['href']
            return r

        except Exception as e:
            print(f"An exception has occured: {e}")
            return None

    def get_survey_details(self):
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {self.config.token}"
        }

        if not self.config.survey_id:
            raise SurveyMonkeyError("There is no survey ID in the class object")

        method = f"/details"
        url = self.config.survey_href + method

        response = requests.request("GET", url, headers=headers)

        if not response.ok or response.status_code in [400, 404]:
            print(url)
            print(response.text)
            raise SurveyMonkeyError("The Survey Monkey API did not respond properly")

        try:
            r = response.json()
            self.config.pages_id = r['pages'][0]['id']
            self.config.pages_href = r['pages'][0]['href']
            return r

        except Exception as e:
            print(f"An exception has occured: {e}")
            return None

    def update_survey_page(self):
        payload = {"title": f"{self.config.survey_page_title}", "description": f"{self.config.survey_page_title}"}

        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {self.config.token}"
        }

        response = requests.request("PATCH", self.config.pages_href, json=payload, headers=headers)

        if not response.ok or response.status_code in [400, 404]:
            print(self.config.pages_href)
            print(response.text)
            raise SurveyMonkeyError("The Survey Monkey API did not respond properly")

        try:
            r = response.json()
            return r

        except Exception as e:
            print(f"An exception has occured: {e}")
            return None


def main():
    print("hello surveymonekey")


if __name__ == "__main__":
    main()
