# -*- coding: utf-8 -*-

import requests
import bs4

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
    BeautifulSoup.find_all = BeautifulSoup.findAll


AVAILABLE_LANGUAGES = {
    'af': ('African', "31"),
    'zh': ('Chinese', "17"),
    'cz': ('Czech', "16"),
    'nl': ('Dutch', "24"),
    'en': ('English', "1"),
    'eo': ('Esperanto', "34"),
    'de': ('German', "3"),
    'gr': ('Greek', "38"),
    'fi': ('Finnish', "36"),
    'fr': ('French', "4"),
    'ga': ('Irish', "49"),
    'it': ('Italian', "23"),
    'la': ('Latin', "37"),
    'jp': ('Japanse', "28"),
    'xal': ('Kalmyk', "35"),
    'ko': ('Korean', "39"),
    'pt': ('Portugese', "11"),
    'ru': ('Russian', "2"),
    'sv': ('Swedish', "29"),
    'sk': ('Slovak', "60"),
    'sl': ('Slovenian', "67"),
    'es': ('Spanish', "5"),
    'ua': ('Ukrainian', "33"),
    'lv': ('Latvian', "27"),
    'et': ('Estonian', "26")
}

def _lookup_language_by_number(language_number):
    for value in AVAILABLE_LANGUAGES.values():
        if (language_number in value):
            return value[0]
            break
        else:
            continue

def _lookup_language_by_country_code(language_country_code):
    return AVAILABLE_LANGUAGES.get(language_country_code)[1]


class UnavailableLanguageError(Exception):
    def __str__(self):
        return "Languages have to be in the following list: {}".format(
            ", ".join(AVAILABLE_LANGUAGES.keys()))


class Result(object):
    def __init__(self, from_lang=None, to_lang=None, translation_tuples=None):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.translation_tuples = list(translation_tuples) \
                                  if translation_tuples else []

    @property
    def n_results(self):
        return len(self.translation_tuples)

class Dict(object):
    @classmethod
    def translate(cls, word, from_language, to_language):
        if any(map(lambda l: l.lower() not in AVAILABLE_LANGUAGES.keys(),
                   [from_language, to_language])):
            raise UnavailableLanguageError

        response_body = cls._get_response(word, from_language, to_language)
        result = cls._parse_response(response_body)

        return cls._correct_translation_order(result, word)

    @classmethod
    def _get_response(cls, word, from_language, to_language):
        try:
            res = requests.get(
                url="https://www.multitran.com/c/M.exe",
                params={
                    "CL": "1",
                    "s": word.encode("utf-8"),
                    "l1": _lookup_language_by_country_code(from_language),
                    "l2": _lookup_language_by_country_code(to_language),
                },
                headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'},
                timeout=0.5  # set a timeout so that requests switches to ipv4 connection early

            )
            return res.content.decode("utf-8")
        except requests.exceptions.ReadTimeout:
            print("Timeout occurred")

    # Quick and dirty: find javascript arrays for input/output words on response body
    @classmethod
    def _parse_response(cls, response_body):
        soup = BeautifulSoup(response_body, "html.parser")
        souptable = soup.find_all("table")[1]  # filter out the table containing the translations form the html page
        trs = souptable.contents

        # Create tuple list with translations
        zip = []  # List of translation tuples
        for tr in trs:
            if type(tr) is bs4.element.Tag and tr.find("td",
                                                       class_="gray"):  # first find all Rows with the from_word as translation input
                from_word_td = tr.find("td",
                                       class_="gray")  # the from_word is within the td element with class gray which is within a tr element
                from_word = (
                            from_word_td.a.string + ", " + from_word_td.em.string)  # extract the text of td and combine

                for sibling in tr.next_siblings:  # in multitrans table structure to_words are on the same hirarchical level (tr) as from_words. Therewith we will look for siblings of the from_word (tr) elements
                    sibling_soup = BeautifulSoup(repr(sibling),
                                                 "html.parser")  # somewhow the siblings are not accessible by python anymore. So I'm using Beautifulsoup again. I'm sure this can be avoided anyhow
                    to_word = ""
                    if sibling_soup.find("td",
                                         class_="gray"):  # stops looking for tr siblings if it finds the next from_word to translate
                        break
                    else:
                        if type(sibling_soup.find("td",
                                                  class_="trans")) is bs4.element.Tag:  # extract to_words from all appropriate rows
                            to_word = (sibling_soup.find("td", class_="trans")).a.string
                            to_word = to_word

                        if type(sibling_soup.find("td",
                                                  class_="subj")) is bs4.element.Tag:  # there are additional informatino for to_word translations which will be added to the to_word
                            addition = (sibling_soup.find("td", class_="subj")).a.string
                            to_word = to_word + " (" + addition + ")"

                            if bool(to_word):  # create the translation tuple only if the to_word is not empty
                                translation_tuple = (to_word, from_word)
                                zip.append(translation_tuple)  # Add translation Tuple to List of Translations

        return Result(
            from_lang=_lookup_language_by_number(soup.find(id="l1")['value']),
            to_lang=_lookup_language_by_number(soup.find(id="l2")['value']),
            translation_tuples=zip,
        )


    # Heuristic: left column is the one with more occurrences of the to-be-translated word
    @classmethod
    def _correct_translation_order(cls, result, word):

        if not result.translation_tuples:
            return result

        [from_words, to_words] = zip(*result.translation_tuples)

        n_from_lang = sum(from_word.lower().count(word.lower()) for from_word in from_words)
        n_to_lang = sum(to_word.lower().count(word.lower()) for to_word in to_words)

        return result if n_from_lang >= n_to_lang \
                      else Result(
                          from_lang=result.from_lang,
                          to_lang=result.to_lang,
                          translation_tuples=zip(to_words, from_words),
                      )