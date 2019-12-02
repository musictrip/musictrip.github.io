#!/usr/bin/env python3
from scraping.response_handling import get_response
from scraping.individual_page_scraper import IndividualPageScraper


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


instruments = ["flute",
               "oboe",
               "clarinet",
               "bassoon",
               "saxophone",
               "french-horn",
               "trumpet",
               "trombone",
               "tuba",
               "violin",
               "viola",
               "cello",
               "double-bass",
               "guitar",
               "piano",
               "organ",
               "voice",
               "chamber-music",
               "conductor"
               ]

if __name__ == "__main__":

    for instrument in instruments:
        classes_page = "https://www.musicalchairs.info/" + instrument + "/courses"
        response = get_response(classes_page)
        class_link_list = extract_list_of_class_links(response)

        page_scraper = IndividualPageScraper()
        for class_link in class_link_list:
            masterclass = page_scraper.extract_masterclass(class_link, instrument)
            if masterclass.is_in_DACH():
                masterclass.save()
