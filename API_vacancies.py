import json
import requests
from abc import ABC, abstractmethod


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class ApiVacancies(ABC):

    @abstractmethod
    def get_vacancies(self, count):
        pass


class Vacancies:
    def __init__(self, keywords: str, salary: int, page):
        self.keywords = keywords
        self.salary = salary
        self.page = page


class HeadHunter(Vacancies, ApiVacancies):

    def __init__(self, keywords: str, salary: int, page):
        super().__init__(keywords, salary, page)
        self.data = None

    def get_vacancies(self):
        self.data = requests.get('https://api.hh.ru/vacancies',
                                 params={'text': self.keywords, 'per_page': self.page}).json()

        return self.data

    def sorting_vacansies(self):

        suitable_vacancies = []

        for vac in self.data["items"]:
            if not ((vac['salary'] is None) or (vac['salary']['from'] is None)):
                if self.salary <= int(vac["salary"]["from"]):
                    if vac["salary"]["to"] is None:
                        zp = f'{vac["salary"]["from"]} {vac["salary"]["currency"]}'
                    else:
                        zp = f'{vac["salary"]["from"]} - {vac["salary"]["to"]} {vac["salary"]["currency"]}'

                    if vac["snippet"]["requirement"] is None:
                        candidat = vac["snippet"]["responsibility"]
                    elif vac["snippet"]["responsibility"] is None:
                        candidat = vac["snippet"]["requirement"]
                    else:
                        candidat = f'{vac["snippet"]["requirement"]}\n{vac["snippet"]["responsibility"]}'

                    vac_info = {
                        "profession": vac["name"],
                        "candidat": candidat,
                        "experience": vac["experience"]["name"],
                        "payment": zp,
                        "url": vac["alternate_url"]
                    }
                    suitable_vacancies.append(vac_info)
        return suitable_vacancies


class SuperJob(Vacancies, ApiVacancies):

    def __init__(self, keywords: str, salary: int, page):
        super().__init__(keywords, salary, page)
        self.data = None

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': "v3.r.137873895.11b1cd08ea1546539ddfe0cade694f7ebb275f7b"
                            ".6abbddfa30520c81d7926cd4fa3cea1c0d8125df",
        }
        self.data = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers,
                                 params={'keywords': self.keywords, 'page': self.page}).json()
        return self.data

    def sorting_vacansies(self):

        suitable_vacancies = []

        for vac in self.data["objects"]:
            if self.salary <= int(vac["payment_from"]):
                if vac["payment_to"] == 0:
                    zp = f'{vac["payment_from"]} {vac["currency"]}'
                else:
                    zp = f'{vac["payment_from"]} - {vac["payment_to"]} {vac["currency"]}'
                vac_info = {
                    "profession": vac["profession"],
                    "candidat": vac["candidat"],
                    "experience": vac["experience"]["title"],
                    "payment": zp,
                    "url": vac["client"]["link"]
                }
                suitable_vacancies.append(vac_info)
        return suitable_vacancies


def load_vacancies(list_vacancies):
    with open("vacancies.json", "w", encoding="UTF-8") as file:
        file.write(json.dumps(list_vacancies, indent=4))


def formatting():
    with open("vacancies.json", "r", encoding="UTF-8") as file:
        item = json.load(file)
        for i in item:
            print(
                f'Профессия: {i["profession"]}\nКраткое описание: {i["candidat"]}\nТребуемый опыт: {i["experience"]}'
                f'\nЗарплата: {i["payment"]}\nСсылка на вакансию: {i["url"]}\n')


# hh = HeadHunter("python", 15000, 3)
# hh.get_vacancies()
# printj(hh.sorting_vacansies())
# load_vacancies(hh.sorting_vacansies())
# formatting()
