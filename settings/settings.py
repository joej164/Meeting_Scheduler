# Settings file for the library
import yaml
from datetime import datetime


class SurveySettingsError(Exception):
    pass


class Settings():
    def __init__(self):
        self.token = None
        self.valid_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.valid_days = list(range(1, 32))
        self.valid_weekdays = ['Friday', 'Saturday', 'Sunday']
        self.valid_years = list(range(2019, 2025))  # Update in 2026
        self.meetup_month = None
        self.meetup_day = None
        self.meetup_weekday = None
        self.meetup_year = None
        self.meetup_time = None
        self.survey_api_url = "https://api.surveymonkey.com/v3/"
        self.survey_month = None
        self.survey_days = None
        self.survey_year = None
        self.survey_weekday = None
        self.survey_title = None
        self.survey_time = None
        self.survey_page_title = None
        self.question_filenames = ["question1.j2", "question2.j2", "question3.j2"]

        self.load_settings()
        self.prompt_for_missing_info()
        self.calculate_and_validate_weekdays()
        self.set_survey_names()
        self.calculate_meeting_time()

    # Load data from the settings.yml file
    def load_settings(self):
        with open("settings.yml", "r") as settings_file:
            data = yaml.safe_load(settings_file)
            for k, v in data.items():
                setattr(self, k, v)

    def set_survey_names(self):
        if not self.survey_title:
            self.survey_title = f"{self.survey_month} {self.survey_year} - PDT Alumni Meetup Test"
        if not self.survey_page_title:
            self.survey_page_title = f"{self.survey_month} {self.survey_year} - PDT Alumni Meetup Test"

    def calculate_and_validate_weekdays(self):
        meetup_weekday = self.calculate_weekday(self.meetup_year, self.meetup_month, self.meetup_day)

        if meetup_weekday not in self.valid_weekdays:
            raise ValueError(f"The day of the next meetup is not in {self.valid_weekdays}")
        else:
            self.meetup_weekday = meetup_weekday

        survey_weekdays = []
        for day in self.survey_days:
            survey_weekdays.append(self.calculate_weekday(self.survey_year, self.survey_month, day))

        if not all(x == survey_weekdays[0] for x in survey_weekdays):
            raise ValueError(f"Not all of the survey days are on the same day")
        else:
            self.survey_weekday = survey_weekdays[0]

    @staticmethod
    def calculate_weekday(year, month, day):
        # Month is the name of the Full Month
        day = datetime.strptime(f"{year} {month} {day}", "%Y %B %d")
        weekday = datetime.strftime(day, "%A")
        return weekday

    def calculate_meeting_time(self):
        # Based on the day of week, return the time of the get together
        day_to_time = {
            "Friday": "7-9pm",
            "Saturday": "6-8pm",
            "Sunday": "1-3pm"
        }

        if self.survey_weekday not in day_to_time.keys():
            raise SurveySettingsError(f"The value '{self.survey_weekday}' was not in the conversion dictionary")
        else:
            self.survey_time = day_to_time[self.survey_weekday]

    def prompt_for_missing_info(self):
        # Prompt the user for any data missing after the settings load
        while self.meetup_month not in self.valid_months:
            month = input("Enter the Month for the next Meetup: ")
            if month not in self.valid_months:
                print(f"Invalid Month!  Enter a month in the following format: {self.valid_months}")
            else:
                self.meetup_month = month

        while self.meetup_day not in self.valid_days:
            try:
                meetup_day = int(input("Enter the day of the month for the next meetup: "))
            except ValueError:
                meetup_day = None

            if meetup_day not in self.valid_days:
                print(f"Invalid Day!  Enter a day in the following format: {self.valid_days}")
            else:
                self.meetup_day = meetup_day

        while self.meetup_year not in self.valid_years:
            try:
                meetup_year = int(input("Enter the year for the next meetup: "))
            except ValueError:
                meetup_year = None

            if meetup_year not in self.valid_years:
                print(f"Enter a valid year from the list of valid years: {self.valid_years}")
            else:
                self.meetup_year = meetup_year

        while self.survey_month not in self.valid_months:
            month = input("Enter the Month for the next Survey: ")
            if month not in self.valid_months:
                print(f"Invalid Month!  Enter a month in the following format: {self.valid_months}")
            else:
                self.survey_month = month

        while not self.survey_days or not all(True if x in self.valid_days else False for x in self.survey_days):
            survey_days = input("Enter the days of the month for the next meetup as numbers seperated by spaces (Ex: 2 4 6): ")
            days = [int(x) for x in survey_days.split() if x.isdigit() and int(x) in self.valid_days]
            if not days:
                print(f"No valid days.  Enter a at least one valid day from the following list: {self.valid_days}")
            else:
                self.survey_days = days

        while self.survey_year not in self.valid_years:
            try:
                survey_year = int(input("Enter the year for the next survey: "))
            except ValueError:
                survey_year = None

            if survey_year not in self.valid_years:
                print(f"Enter a valid year from the list of valid years: {self.valid_years}")
            else:
                self.survey_year = survey_year
