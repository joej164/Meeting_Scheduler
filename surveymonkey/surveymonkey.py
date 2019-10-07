# Functions and files to work with Survey Monkey
import requests
import jinja2
import json


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

    def add_survey_questions(self):
        url = self.config.pages_href + "/questions"
        print(f"add question url is: {url}")
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {self.config.token}"
        }

        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)

        responses = []
        # Load the template from file system
        for template_file in self.config.question_filenames:
            template = template_env.get_template(template_file)
            rendered_template = template.render(
                day_list=self.config.survey_days,
                weekday=self.config.survey_weekday,
                year=self.config.survey_year,
                month=self.config.survey_month,
                time=self.config.survey_time)

            payload = json.loads(rendered_template)
            print('$$$$$$$$ in template_file $$$$$$$$$')
            print(payload)

            response = requests.request("POST", url, json=payload, headers=headers)

            if not response.ok or response.status_code in [400, 404]:
                print(self.config.pages_href)
                print(response.text)
                raise SurveyMonkeyError("The Survey Monkey API did not respond properly")

            try:
                r = response.json()
                responses.append(r)

            except Exception as e:
                print(f"An exception has occured: {e}")
                return None

        return responses

    def create_collector(self):
        url = self.config.survey_href + "/collectors"

        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {self.config.token}"
        }

        payload = {
            "type": "weblink",
            "name": f"{self.config.survey_title} Collector"
            }

        response = requests.request("POST", url, json=payload, headers=headers)

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
