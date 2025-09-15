import requests
import urllib3
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from random_num import random_number


urllib3.disable_warnings(InsecureRequestWarning)

URL_SUBJECTS = "https://ege.fipi.ru/bank/"
URL_TASKS = "https://ege.fipi.ru/bank/questions.php?proj="

def load_subjects():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(URL_SUBJECTS, verify=False, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    subjects = []
    for subject in soup.find_all("li"):
        onclick = subject["onclick"]
        index = onclick.rfind('"')
        c = subject["onclick"][15:index]
        subjects += [{"title": subject.text, "data": c}]
    return subjects

def load_tasks(project):
    h = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(URL_TASKS + project + "&page=" + random_number() + "&pagesize=" + random_number(), verify=False, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    tasks = soup.find_all('div', class_='qblock')
    for task in tasks:
        b = task.find_all('p', class_='MsoNormal')
        task_text = task.text.split("\n")
        # print(len(task_text))

        for i in task_text:
            n_i = i.strip()
            if len(n_i) != 0:
                h += n_i + "\n"
        # print(task.text)
        # for p in b:
        #     print(p.text)
        # break
    return h




load_tasks("B9ACA5BBB2E19E434CD6BEC25284C67F")