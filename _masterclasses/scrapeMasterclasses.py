#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()


class Masterclass:
    country = ""
    city = ""
    masterclass_link = ""
    title = ""
    start_date = ""
    end_date = ""
    description_english = ""
    description_chinese = ""

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


def get_response(site: str):
    """
    Get the parsed beautiful soup from a site link
    :param site: Site link as string
    :return: Parsed beautiful soup response
    """
    try:
        request = requests.get(site)
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Request error for site " + site)

    if request.status_code != 200:
        raise RuntimeError("Status code error for site " + site)

    try:
        return BeautifulSoup(request.content, "html.parser")
    except Exception as e:
        raise RuntimeError("Parsing error for site " + site)


def extract_list_of_class_links(response):
    """
    Extract the individual class links from the overview page
    :param response: Response containing the overview page
    :return: List of strings containing all class subpages
    """
    class_links = []
    for preview in response.findAll("li", {"class": "preview"}):
        class_links += [preview.a.get("href")]

    return class_links


def extract_city_and_country(response, class_page):
    # Extract city and country from 'post_item_location' field
    try:
        full_location: str = response.find("div", {"class": "post_item_location"}).text
        city, country = [s.strip() for s in full_location.split(",")]
        return city, country
    except:
        print("Failed to extract city and country for site " + class_page)


def extract_masterclass_link(response, class_page):
    try:
        link: str = response.find("div", {"class": "post_image_box"}).a.get("href").strip()
        # Since musicalchairs is redirecting to the masterclass, we do another request to extract the URL
        return requests.get(link).url
    except:
        print("Failed to extract masterclass link for site " + class_page)


def extract_title(response, class_page):
    try:
        title: str = response.find("div", {"class": "post_item_name"}).h1.text
        return title
    except:
        print("Failed to extract masterclass title for site " + class_page)


def spelled_month_to_number(month_string):
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


def extract_date(response, class_page):
    # TODO Do the right thing for dates that span multiple months
    try:
        full_date: str = response.find("div", {"class": "post_item_info"}).h2.text
        days_and_month, year = [s.strip() for s in full_date.split(",")]

        day_begin, _, day_end, month_string = days_and_month.split(" ")
        month = spelled_month_to_number(month_string)

        sep = "-"
        start_date = year + sep + month + sep + day_begin
        end_date = year + sep + month + sep + day_end
        return start_date, end_date
    except:
        print("Failed to extract masterclass date for site " + class_page)


def extract_description(response, class_page):
    try:
        description_english: str = response.find("div", {"class": "post_item_desc"}).text
        description_english = description_english.replace(".", ". ")

        description_chinese = translator.translate(description_english, dest="zh-TW").text

        return description_english, description_chinese
    except:
        print("Failed to extract masterclass description for site " + class_page)


def extract_masterclass(class_page):
    try:
        response = get_response(class_page)
    except:
        print("Failed extracting masterclass for site: " + class_page)
        return

    masterclass = Masterclass()

    masterclass.city, masterclass.country = extract_city_and_country(response, class_page)
    masterclass.masterclass_link = extract_masterclass_link(response, class_page)
    masterclass.title = extract_title(response, class_page)
    masterclass.start_date, masterclass.end_date = extract_date(response, class_page)
    masterclass.description_english, masterclass.description_chinese = extract_description(response, class_page)
    return masterclass


class_page = "https://www.musicalchairs.info/courses/5530?ref=21"
print(extract_masterclass(class_page))
