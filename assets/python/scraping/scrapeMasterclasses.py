#!/usr/bin/env python3
from pathlib import Path
import yaml
from typing import Set
from assets.python.scraping.masterclass import Masterclass
from assets.python.scraping.response_handling import get_response
from assets.python.scraping.individual_page_scraper import IndividualPageScraper


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


def existing_masterclasses() -> Set[Masterclass]:
    """
    Get a set of all existing masterclasses from the _masterclasses folder
    :return: Set of existing masterclasses
    """
    masterclass_folder = Path.cwd().parent.parent.parent.joinpath("_masterclasses")
    s = set()
    for masterclass_file in masterclass_folder.glob("*.md"):
        try:
            parsed_masterclass = Masterclass.from_markdown_file(masterclass_file)
            s.add(parsed_masterclass)
        except yaml.YAMLError as e:
            print(e)
    return s


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
    existing_masterclasses = existing_masterclasses()

    for instrument in instruments:
        classes_page = "https://www.musicalchairs.info/" + instrument + "/courses"
        response = get_response(classes_page)
        class_link_list = extract_list_of_class_links(response)

        page_scraper = IndividualPageScraper()
        for class_link in class_link_list:
            masterclass = page_scraper.extract_masterclass(class_link, instrument)
            if masterclass.is_in_DACH() and masterclass not in existing_masterclasses:
                masterclass.save()
