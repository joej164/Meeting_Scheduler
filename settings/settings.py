# Settings file for the library

import yaml


class Settings():
    def __init__(self):
        self.token = None
        self.valid_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.valid_days = list(range(1, 32))
        self.valid_years = list(range(2019, 2025))  # Will need updating in 2026
        self.meetup_month = None
        self.meetup_day = None
        self.meetup_year = None
        self.survey_month = None
        self.survey_days = None
        self.survey_year = None
        self.load_settings()
        self.prompt_for_missing_info()

    # Load data from the settings.yml file
    def load_settings(self):
        with open("settings.yml", "r") as settings_file:
            data = yaml.safe_load(settings_file)
            for k, v in data.items():
                setattr(self, k, v)

    # Prompt the user for any data missing after the settings load
    def prompt_for_missing_info(self):
        while self.meetup_month not in self.valid_months:
            month = input("Enter the Month for the next Meetup: ")
            if month not in self.valid_months:
                print(f"Invalid Month!  Enter a month in the following format: {self.valid_months}")
            else:
                self.meetup_month = month

        # Prompt the user for the Month of the next proposed survey
        while self.survey_month not in self.valid_months:
            month = input("Enter the Month for the next Survey: ")
            if month not in self.valid_months:
                print(f"Invalid Month!  Enter a month in the following format: {self.valid_months}")
            else:
                self.survey_month = month

        # Prompt the user for the day of the next meetup
        while not self.meetup_day:
            meetup_day = input("Enter the day of the month for the next meetup: ")
            if meetup_day not in self.valid_days:
                print(f"Invalid Day!  Enter a day in the following format: {self.valid_days}")
            else:
                self.meetup_day = meetup_day

        # Prompt the user for the possible days of the next survey
        while not self.survey_days:
            meetup_days = input("Enter the days of the month for the next meetup as numbers seperated by spaces (Ex: 2 4 6): ")
            days = [x for x in meetup_days.split() if x in self.valid_days]
            if not days:
                print(f"No valid days.  Enter a at least one valid day from the following list: {self.valid_days}")
            else:
                self.survey_days = days

        while not self.meetup_year:
            meetup_year = input("Enter the year for the next meetup: ")
            if meetup_year not in self.valid_years:
                print(f"Enter a valid year from the list of valid years: {self.valid_years}")
            else:
                self.meetup_year = meetup_year

        while not self.survey_year:
            survey_year = input("Enter the year for the next survey: ")
            if survey_year not in self.valid_years:
                print(f"Enter a valid year from the list of valid years: {self.valid_years}")
            else:
                self.survey_year = survey_year


