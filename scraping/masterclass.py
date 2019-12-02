import os


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
        return {"country": self.country, "city": self.city, "masterclass_link": self.masterclass_link,
                "title": self.title, "start_date": self.start_date, "end_date": self.end_date,
                "description_english": self.description_english, "description_chinese": self.description_chinese}

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
