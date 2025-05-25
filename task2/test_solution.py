import os
import csv
import unittest
from unittest.mock import patch, Mock

import requests

from solution import get_animals_by_letter, save_to_csv


class TestAnimalScraper(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <div id="mw-pages">
            <ul>
                <li>Акула</li>
                <li>Бабочка</li>
                <li>Волк</li>
                <li>Гепард</li>
                <li>Дельфин</li>
                <li>Ёж</li>
                <li>Жираф</li>
                <li>Зебра</li>
                <li>Игуана</li>
                <li>Йоркширский терьер</li>
            </ul>
            <a href="/wiki/Категория:Животные_по_алфавиту?pagefrom=К">Следующая страница</a>
        </div>
        """

        self.sample_html_page2 = """
        <div id="mw-pages">
            <ul>
                <li>Кошка</li>
                <li>Лев</li>
                <li>Медведь</li>
            </ul>
        </div>
        """

    @patch("requests.get")
    def test_get_animals_by_letter(self, mock_get):
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.text = self.sample_html
        mock_response1.encoding = "utf-8"

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.text = self.sample_html_page2
        mock_response2.encoding = "utf-8"

        mock_get.side_effect = [mock_response1, mock_response2]

        result = get_animals_by_letter()

        self.assertEqual(result["А"], 1)
        self.assertEqual(result["Б"], 1)
        self.assertEqual(result["В"], 1)
        self.assertEqual(result["Г"], 1)
        self.assertEqual(result["Д"], 1)
        self.assertEqual(result["Ё"], 1)
        self.assertEqual(result["Ж"], 1)
        self.assertEqual(result["З"], 1)
        self.assertEqual(result["И"], 1)
        self.assertEqual(result["Й"], 1)
        self.assertEqual(result["К"], 1)
        self.assertEqual(result["Л"], 1)
        self.assertEqual(result["М"], 1)

        self.assertEqual(mock_get.call_count, 2)

    @patch("requests.get")
    def test_get_animals_by_letter_error_handling(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_animals_by_letter()

    def test_save_to_csv(self):
        test_counts = {"А": 5, "Б": 3, "В": 2}

        save_to_csv(test_counts)

        self.assertTrue(os.path.exists("beasts.csv"))

        with open("beasts.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ["А", "5"])
        self.assertEqual(rows[1], ["Б", "3"])
        self.assertEqual(rows[2], ["В", "2"])

        os.remove("beasts.csv")

    def test_save_to_csv_sorting(self):
        test_counts = {"В": 2, "А": 5, "Б": 3}

        save_to_csv(test_counts)

        with open("beasts.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertEqual(rows[0][0], "А")
        self.assertEqual(rows[1][0], "Б")
        self.assertEqual(rows[2][0], "В")

        os.remove("beasts.csv")

    @patch("requests.get")
    def test_get_animals_by_letter_empty_page(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<div id='mw-pages'><ul></ul></div>"
        mock_response.encoding = "utf-8"
        mock_get.return_value = mock_response

        result = get_animals_by_letter()
        self.assertEqual(len(result), 0)

    @patch("requests.get")
    def test_get_animals_by_letter_no_next_page(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <div id="mw-pages">
            <ul>
                <li>Акула</li>
                <li>Бабочка</li>
            </ul>
        </div>
        """
        mock_response.encoding = "utf-8"
        mock_get.return_value = mock_response

        result = get_animals_by_letter()
        self.assertEqual(result["А"], 1)
        self.assertEqual(result["Б"], 1)
        self.assertEqual(mock_get.call_count, 1)

    @patch("requests.get")
    def test_get_animals_by_letter_non_russian_chars(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <div id="mw-pages">
            <ul>
                <li>Акула</li>
                <li>123</li>
                <li>!@#</li>
                <li>Бабочка</li>
            </ul>
        </div>
        """
        mock_response.encoding = "utf-8"
        mock_get.return_value = mock_response

        result = get_animals_by_letter()
        self.assertEqual(result["А"], 1)
        self.assertEqual(result["Б"], 1)
        self.assertEqual(len(result), 2)

    def test_save_to_csv_empty_data(self):
        test_counts = {}
        save_to_csv(test_counts)

        self.assertTrue(os.path.exists("beasts.csv"))
        with open("beasts.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 0)
        os.remove("beasts.csv")

    @patch("requests.get")
    def test_get_animals_by_letter_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()

        with self.assertRaises(requests.exceptions.Timeout):
            get_animals_by_letter()


if __name__ == "__main__":
    unittest.main()
