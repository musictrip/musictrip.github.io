import os
from typing import Tuple
import yaml


class Masterclass:
    country = ""
    city = ""
    masterclass_link = ""
    title = ""
    start_date = ""
    end_date = ""
    description_english = ""
    description_chinese = ""
    original_link = ""
    instrument = ""
    professor = ""
    professor_link = ""

    def __repr__(self):
        sep = ", "
        return "{" + "country:" + self.country + sep \
               + "city:" + self.city + sep \
               + "masterclass_link:" + self.masterclass_link + sep \
               + "title:" + self.title + sep \
               + "start_date:" + self.start_date + sep \
               + "end_date:" + self.end_date + sep \
               + "description_english:" + self.description_english + sep \
               + "description_chinese:" + self.description_chinese + "}"

    def __str__(self):
        sep = ", \n"
        return "Masterclass(" + self.title + sep \
               + self.city + sep \
               + self.country + sep \
               + self.masterclass_link + sep + \
               self.start_date + sep \
               + self.end_date + sep \
               + self.description_english + sep \
               + self.description_chinese + ")"

    def __eq__(self, other):
        start_dates_equal = self.__date_equal(self.start_date, other.start_date)
        end_dates_equal = self.__date_equal(self.end_date, other.end_date)
        dates_equal = start_dates_equal and end_dates_equal

        own_city = self.city.strip().lower()
        other_city = other.city.strip().lower()
        cities_equal = own_city == other_city

        own_country = self.country.strip().lower()
        other_country = other.country.strip().lower()
        country_equal = own_country == other_country

        return dates_equal and cities_equal and country_equal

    def __date_equal(self, own_date, other_date):
        try:
            year_own, month_own, day_own = self.__split_date(own_date)
            year_other, month_other, day_other = self.__split_date(other_date)

            if year_own != year_other or month_own != month_other or day_own != day_other:
                return False
        except ValueError:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.start_date, self.end_date, self.city.strip().lower(), self.country.strip().lower()))

    def __split_date(self, date: str) -> Tuple[int, int, int]:
        year_month_day = date.split("-")
        if len(year_month_day) != 3:
            raise ValueError("Date not parseable.")
        year, month, day = year_month_day
        return int(year), int(month), int(day)

    @staticmethod
    def from_markdown_file(markdown_file):
        masterclass = Masterclass()
        try:
            with open(markdown_file) as file:
                parsed_yaml = next(yaml.safe_load_all(file))

                masterclass.country = parsed_yaml["country"]
                masterclass.city = parsed_yaml["city"]
                masterclass.title = parsed_yaml["title"]
                masterclass.professor = parsed_yaml["teachers"][0]["name"]
                masterclass.professor_link = parsed_yaml["teachers"][0]["link"]
                masterclass.start_date = str(parsed_yaml["startDate"])
                masterclass.end_date = str(parsed_yaml["endDate"])
                masterclass.instrument = parsed_yaml["instruments"][0]
                masterclass.masterclass_link = parsed_yaml["masterclassLink"]
        except:
            print("Failed parsing markdown file " + markdown_file)
        return masterclass

    def save(self):
        """
        Save this masterclass to a Markdown file that can be parsed by jekyll
        :return: None
        """
        title_without_spaces = "".join(self.title.split())
        file_name = "scraped_masterclasses" + os.sep + title_without_spaces + ".md"

        # Maybe create folder to hold files
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except:
                return

        with open(file_name, "w") as file:
            endl = "\n"
            lines = [
                "---",
                "title: " + self.title,
                "teachers:",
                "\t- name: " + self.professor,
                "\t  link: " + self.professor_link,
                "fee: TODO",
                "feeExplanation: ",
                "\t- TODO",
                "startDate: " + self.start_date,
                "endDate: " + self.end_date,
                "city: " + self.city,
                "country: " + self.__country_to_chinese(self.country),
                "instruments:",
                "\t- " + self.instrument,
                "\t- TODO",
                "registrationLink: TODO",
                "masterclassLink: " + self.masterclass_link,
                "---",
                "Original link: " + self.original_link,
                "English description:",
                self.description_english.replace(". ", ".\n") + endl,
                "Chinese description:",
                self.description_chinese.replace("。", "。\n")
            ]
            file.writelines([line + endl for line in lines])
            print("Scraped " + self.masterclass_link)

    def is_in_DACH(self):
        """
        Find our whether the masterclass is in one of the three countries we allow
        :return: Is the masterclass in Austria, Germany or Switzerland?
        """
        country_without_spaces = "".join(self.country.split()).lower()
        return country_without_spaces in ["germany", "austria", "switzerland"]

    def __country_to_chinese(self, country: str) -> str:
        """
        Translate a country string to Chinese
        :param country: Country as string
        :return: Country translated to Chinese
        """
        country_without_spaces = "".join(country.split()).lower()
        if country_without_spaces == "germany":
            return "德國"
        if country_without_spaces == "austria":
            return "奧地利"
        if country_without_spaces == "switzerland":
            return "瑞士"

        return "Unknown"
