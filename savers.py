from abc import ABC, abstractmethod
from vacancy import Vacancy, Vacancies
import json


class Saver(ABC):
    """Абстрактный класс для редактирования и обработки списка вакансий"""

    @abstractmethod
    def save_vacancies(self):
        pass

    def read_vacancies(self):
        pass


class JSONSaver(Vacancies, Saver):
    """Класс для обработки списка вакансий в JSON формате"""

    def save_vacancies(self):
        with open('vacancies.json', 'w') as fh:
            json.dump(self.to_list_dict(), fh)

    def read_vacancies(self):
        with open('vacancies.json', 'r') as fh:
            list_dict = json.load(fh)
        self.__all_vacancies = []
        for i in list_dict:
            self.all_vacancies.append(Vacancy.from_dict(i))