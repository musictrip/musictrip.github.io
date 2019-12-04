import requests
from googletrans import Translator
import googlesearch
from assets.python.scraping.masterclass import Masterclass
from assets.python.scraping.response_handling import get_response
from parse import *
import nltk
from nltk.tag.stanford import StanfordNERTagger
from typing import Tuple
import time


class IndividualPageScraper:
    translator = Translator()
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz', "stanford-ner.jar")

    def __extract_date(self, response, class_page):
        try:
            full_date: str = response.find("div", {"class": "post_item_info"}).h2.text
            sep = "-"

            # Date is of format dd - dd mmm, yyyy
            if len(full_date.split(" ")) == 5:
                day_begin, day_end, month, year = parse("{} - {} {}, {}", full_date)
                month = self.__spelled_month_to_number(month)
                start_date = year + sep + month + sep + day_begin
                end_date = year + sep + month + sep + day_end
                return start_date, end_date

            # Date is of format dd mmm - dd mmm, yyyy
            if len(full_date.split(" ")) == 6:
                day_begin, month_begin, day_end, month_end, year = parse("{} {} - {} {}, {}", full_date)
                month_begin = self.__spelled_month_to_number(month_begin)
                month_end = self.__spelled_month_to_number(month_end)
                start_date = year + sep + month_begin + sep + day_begin
                end_date = year + sep + month_end + sep + day_end
                return start_date, end_date

            # Date is of format dd mmm yyyy - dd mmm yyyy
            if len(full_date.split(" ")) == 7:
                day_begin, month_begin, year_begin, day_end, month_end, year_end = parse("{} {} {} - {} {} {}",
                                                                                         full_date)
                month_begin = self.__spelled_month_to_number(month_begin)
                month_end = self.__spelled_month_to_number(month_end)
                start_date = year_begin + sep + month_begin + sep + day_begin
                end_date = year_end + sep + month_end + sep + day_end
                return start_date, end_date

            return "TODO", "TODO"

        except:
            print("Failed to extract masterclass date for site " + class_page)

    def __extract_description(self, response, class_page):
        description_english = ""
        description_chinese = ""

        try:
            description_english: str = response.find("div", {"class": "post_item_desc"}).text
            description_english = description_english.replace(".", ". ")
        except:
            print("Failed to extract masterclass description for site " + class_page)

        try:
            description_chinese = self.translator.translate(description_english, dest="zh-TW").text
        except:
            print("Failed to translate masterclass description for site " + class_page)

        return description_english, description_chinese

    def __extract_city_and_country(self, response, class_page):
        # Extract city and country from 'post_item_location' field
        try:
            full_location: str = response.find("div", {"class": "post_item_location"}).text
            city, country = [s.strip() for s in full_location.rsplit(",", maxsplit=1)]
            return city, country
        except:
            print("Failed to extract city and country for site " + class_page)

    def __extract_masterclass_link(self, response, class_page):
        try:
            link: str = response.find("div", {"class": "post_image_box"}).a.get("href").strip()
            # Since musicalchairs is redirecting to the masterclass, we do another request to extract the URL
            return requests.get(link).url
        except:
            print("Failed to extract masterclass link for site " + class_page)
            return class_page + "(TODO enter real link)"

    def __extract_title(self, response, class_page):
        try:
            title: str = response.find("div", {"class": "post_item_name"}).h1.text
            return title
        except:
            print("Failed to extract masterclass title for site " + class_page)

    def __spelled_month_to_number(self, month_string):
        if month_string == "Jan":
            return "01"
        if month_string == "Feb":
            return "02"
        if month_string == "Mar":
            return "03"
        if month_string == "Apr":
            return "04"
        if month_string == "May":
            return "05"
        if month_string == "Jun":
            return "06"
        if month_string == "Jul":
            return "07"
        if month_string == "Aug":
            return "08"
        if month_string == "Sep":
            return "09"
        if month_string == "Oct":
            return "10"
        if month_string == "Nov":
            return "11"
        if month_string == "Dec":
            return "12"

    def __get_first_name(self, text: str) -> str:
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = self.st.tag(tokens)

            # Group words by whether they denote a person name
            output = [[]]
            for a, b in zip([float('nan')] + tags, tags):
                try:
                    if a[1] != b[1]:
                        output.append([])
                except:
                    pass

                if b[1] == "PERSON":
                    output[-1].append(b[0])
            output = [x for x in output if len(x) > 0]

            # Return the first found name
            if len(output) > 0:
                return " ".join(output[0])

            return ""

    def __get_professor_name_and_link(self, title: str, description: str) -> Tuple[str, str]:
        text = title + " " + description
        name = self.__get_first_name(text)

        if name == "":
            return "TODO", "TODO"
        try:
            link = next(googlesearch.search(name + " music"))
            # The google server blocks our scraper if it sends too many requests too fast.
            # Each time we send a request, we wait for a second to circumvent this issue.
            time.sleep(1)
        except:
            print("Failed to search for professor link")
            return name, "TODO"
        return name, link

    def extract_masterclass(self, class_page: str, instrument: str) -> Masterclass:
        try:
            response = get_response(class_page)
        except:
            print("Failed extracting masterclass for site: " + class_page)
            return Masterclass()

        masterclass = Masterclass()
        masterclass.instrument = self.__instrument_to_chinese(instrument)
        masterclass.original_link = class_page
        masterclass.city, masterclass.country = self.__extract_city_and_country(response, class_page)
        if not masterclass.is_in_DACH():
            return masterclass
        masterclass.masterclass_link = self.__extract_masterclass_link(response, class_page)
        masterclass.title = self.__extract_title(response, class_page)
        masterclass.start_date, masterclass.end_date = self.__extract_date(response, class_page)
        masterclass.description_english, masterclass.description_chinese = self.__extract_description(response,
                                                                                                      class_page)
        masterclass.professor, masterclass.professor_link = self.__get_professor_name_and_link(masterclass.title,
                                                                                               masterclass.description_english)

        return masterclass

    def __instrument_to_chinese(self, instrument: str):
        instrument_map = {
            "flute": "長笛",
            "oboe": "雙簧管",
            "clarinet": "單簧管",
            "bassoon": "低音管",
            "saxophone": "薩克斯風",
            "french-horn": "法國號",
            "trumpet": "小號",
            "trombone": "長號",
            "tuba": "低音號",
            "violin": "小提琴",
            "viola": "中提琴",
            "cello": "大提琴",
            "double-bass": "低音提琴",
            "guitar": "吉他",
            "piano": "鋼琴",
            "organ": "管風琴",
            "conductor": "指揮",
            "voice": "聲樂",
            "chamber-music": "室內樂"
        }

        if instrument in instrument_map:
            return instrument_map[instrument]

        return "TODO"
