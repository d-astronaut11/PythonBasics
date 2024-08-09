import os
import random
from faker import Faker
import file_operations 

FAKE = Faker("ru_RU")
SOURCE_FILE_PATH = "src/charsheet.svg"
SKILLS_LIST = [
    "Стремительный прыжок", 
    "Электрический выстрел", 
    "Ледяной удар", 
    "Стремительный удар", 
    "Кислотный взгляд", 
    "Тайный побег",
    "Ледяной выстрел", 
    "Огненный заряд"
]
LETTERS = {
    'а': 'а͠',
    'б': 'б̋',
    'в': 'в͒͠',
    'г': 'г͒͠',
    'д': 'д̋',
    'е': 'е͠',
    'ё': 'ё͒͠',
    'ж': 'ж͒',
    'з': 'з̋̋͠',
    'и': 'и',
    'й': 'й͒͠',
    'к': 'к̋̋',
    'л': 'л̋͠',
    'м': 'м͒͠',
    'н': 'н͒',
    'о': 'о̋',
    'п': 'п̋͠',
    'р': 'р̋͠',
    'с': 'с͒',
    'т': 'т͒',
    'у': 'у͒͠',
    'ф': 'ф̋̋͠',
    'х': 'х͒͠',
    'ц': 'ц̋',
    'ч': 'ч̋͠',
    'ш': 'ш͒͠',
    'щ': 'щ̋',
    'ъ': 'ъ̋͠',
    'ы': 'ы̋͠',
    'ь': 'ь̋',
    'э': 'э͒͠͠',
    'ю': 'ю̋͠',
    'я': 'я̋',
    'А': 'А͠',
    'Б': 'Б̋',
    'В': 'В͒͠',
    'Г': 'Г͒͠',
    'Д': 'Д̋',
    'Е': 'Е',
    'Ё': 'Ё͒͠',
    'Ж': 'Ж͒',
    'З': 'З̋̋͠',
    'И': 'И',
    'Й': 'Й͒͠',
    'К': 'К̋̋',
    'Л': 'Л̋͠',
    'М': 'М͒͠',
    'Н': 'Н͒',
    'О': 'О̋',
    'П': 'П̋͠',
    'Р': 'Р̋͠',
    'С': 'С͒',
    'Т': 'Т͒',
    'У': 'У͒͠',
    'Ф': 'Ф̋̋͠',
    'Х': 'Х͒͠',
    'Ц': 'Ц̋',
    'Ч': 'Ч̋͠',
    'Ш': 'Ш͒͠',
    'Щ': 'Щ̋',
    'Ъ': 'Ъ̋͠',
    'Ы': 'Ы̋͠',
    'Ь': 'Ь̋',
    'Э': 'Э͒͠͠',
    'Ю': 'Ю̋͠',
    'Я': 'Я̋',
    ' ': ' '
}


def create_folder_if_not_exists(folder_path):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_path)
    os.makedirs(path, exist_ok=True)
    return path


def translate_skills(skills_list):
    final_list =[]
    for skill in skills_list:
        for letter in skill:
            skill = skill.replace(letter, LETTERS[letter])
        final_list.append(skill)
    return final_list


def form_context(skills):
    context = {
        "first_name": FAKE.first_name(),
        "last_name": FAKE.last_name_male(),
        "job": FAKE.job(),
        "town": FAKE.city(),
        "strength": random.randint(3, 18),
        "agility": random.randint(3, 18),
        "endurance": random.randint(3, 18),
        "intelligence": random.randint(3, 18),
        "luck": random.randint(3, 18),
        "skill_1": skills[0],
        "skill_2": skills[1],
        "skill_3": skills[2]
    }
    return context


def main():
    results_path = create_folder_if_not_exists('results')

    for character in range(10):
        skills = random.sample(SKILLS_LIST, 3)
        runic_skills = translate_skills(skills)
        context = form_context(runic_skills)
        
        new_file_path = f'{results_path}/result_{character}.svg'
        file_operations.render_template(SOURCE_FILE_PATH, new_file_path, context)


if __name__ == '__main__':
    main()
    
