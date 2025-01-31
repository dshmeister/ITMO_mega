import requests
import concurrent.futures
import time
import pandas as pd

# Адрес сервиса
URL = "http://78.111.88.52:13001/api/request"



# Вопросы про ИТМО
QUESTIONS = [
  {"query": "В каком году был основан Университет ИТМО?\n1. 1899\n2. 1900\n3. 1920\n4. 1950", "id": 1},
  {"query": "Какой девиз у Университета ИТМО?\n1. Разум, Созидание, Будущее\n2. Наука, Технологии, Прогресс\n3. Больше чем университет\n4. Учись, создавай, меняй мир", "id": 2},
  {"query": "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород", "id": 3},
  {"query": "Какой факультет ИТМО специализируется на информационной безопасности?\n1. Факультет программной инженерии и компьютерных систем\n2. Факультет информационной безопасности\n3. Факультет биотехнологий\n4. Факультет управления", "id": 4},
  {"query": "Какая лаборатория в ИТМО занимается квантовыми технологиями?\n1. Лаборатория искусственного интеллекта\n2. Лаборатория квантовой информатики\n3. Лаборатория компьютерного зрения\n4. Лаборатория биотехнологий", "id": 5},
  {"query": "Как называется знаменитый студенческий конкурс ИТМО по программированию?\n1. ICPC\n2. Codeforces Challenge\n3. ACM ITMO Battle\n4. Google Hash Code", "id": 6},
  {"query": "Какой рейтинг QS World University Rankings занимает ИТМО в 2024 году?\n1. 201-250\n2. 300-350\n3. 400-450\n4. 500-550", "id": 7},
  {"query": "Какой проект запустил ИТМО в сфере кибербезопасности?\n1. CTF ITMO\n2. ITMO SecureNet\n3. ITMO Cybersecurity Hub\n4. Cyber Defense Academy", "id": 8},
  {"query": "В каком международном конкурсе по искусственному интеллекту участвуют студенты ИТМО?\n1. Kaggle AI Challenge\n2. NeurIPS Competition\n3. ImageNet Challenge\n4. AI Hackathon", "id": 9},
  {"query": "Какой статус имеет ИТМО в системе российских вузов?\n1. Исследовательский университет\n2. Инновационный институт\n3. Национальный исследовательский университет\n4. Государственный технологический университет", "id": 10},
  {"query": "Какой проект в ИТМО связан с робототехникой?\n1. ITMO Robotics Lab\n2. AI & Robotics Center\n3. ITMO RoboCup\n4. Cyber Robotics Lab", "id": 11},
  {"query": "Какой предмет на олимпиадах часто выбирают студенты ИТМО?\n1. Физика\n2. Математика\n3. Химия\n4. Биология", "id": 12},
  {"query": "Как называется научный парк Университета ИТМО?\n1. ITMO Science Park\n2. ITMO Technopark\n3. ITMO Innovation Hub\n4. ITMO Digital Valley", "id": 13},
  {"query": "Какой грант выиграл Университет ИТМО в 2022 году?\n1. Грант Сколково\n2. Грант Министерства науки\n3. Грант 'Приоритет 2030'\n4. Грант AI Development", "id": 14},
  {"query": "С каким международным университетом сотрудничает ИТМО в области квантовых технологий?\n1. MIT\n2. ETH Zurich\n3. University of Cambridge\n4. TU Delft", "id": 15},
  {"query": "Как называется официальный сайт Университета ИТМО?\n1. www.itmo.ru\n2. www.itmo.edu\n3. www.itmo.ac\n4. www.itmo.org", "id": 16},
  {"query": "Какая специальность наиболее популярна среди студентов ИТМО?\n1. Программная инженерия\n2. Информационная безопасность\n3. Квантовые технологии\n4. Робототехника", "id": 17},
  {"query": "Как называется программа международного обмена в ИТМО?\n1. ITMO Global Exchange\n2. ITMO International Mobility\n3. ITMO Study Abroad\n4. ITMO Worldwide", "id": 18},
  {"query": "Сколько студентов обучается в Университете ИТМО?\n1. 5 000\n2. 10 000\n3. 15 000\n4. 20 000", "id": 19},
  {"query": "Как называется AI-инициатива в ИТМО?\n1. ITMO AI Lab\n2. ITMO Digital Mind\n3. ITMO DeepTech\n4. AI Research Hub", "id": 20},
  {"query": "Какой факультет в ИТМО отвечает за блокчейн-технологии?\n1. Факультет информационной безопасности\n2. Факультет цифровых финансов\n3. Факультет инновационных технологий\n4. Факультет программной инженерии", "id": 21},
  {"query": "Какой партнер сотрудничает с ИТМО по развитию квантовых вычислений?\n1. Google Quantum AI\n2. IBM Q\n3. Microsoft Quantum\n4. Intel Quantum Lab", "id": 22},
  {"query": "Какой новый кампус строит ИТМО?\n1. ITMO High-Tech Campus\n2. ITMO Innovation Valley\n3. ITMO Digital Hub\n4. ITMO Quantum Park", "id": 23},
  {"query": "Какой международный форум по науке организует ИТМО?\n1. ITMO Science Conference\n2. ITMO Future Forum\n3. ITMO Open Science\n4. ITMO Innovations", "id": 24},
  {"query": "Какой факультет занимается биоинформатикой?\n1. Факультет биотехнологий\n2. Факультет компьютерных наук\n3. Факультет математики\n4. Факультет цифровых технологий", "id": 25}
]

# Функция отправки запроса
def send_request(question):
    start_time = time.time()
    response = requests.post(URL, params=question)
    end_time = time.time()
    elapsed_time = end_time - start_time

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Не JSON", "raw_response": response.text}

    return question["id"], response.status_code, elapsed_time, response_json

# Функция стресс-тестирования
def run_stress_test(batch_size, iterations):
    results = []
    total_time = 0

    print(f"\n🔥 Запуск {iterations} тестов по {batch_size} запросов одновременно 🔥")

    for i in range(iterations):
        batch = QUESTIONS[:batch_size]
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            batch_results = list(executor.map(send_request, batch))

        for req_id, status, elapsed_time, response_json in batch_results:
            results.append({
                "Запрос ID": req_id,
                "HTTP Код": status,
                "Время выполнения (сек)": round(elapsed_time, 4),
                "Ответ JSON?": isinstance(response_json, dict),
                "Ответ сервера": response_json
            })
            total_time += elapsed_time

        print(f"🟢 Итерация {i+1}/{iterations} завершена!")

    return results, total_time

# Запускаем тесты
final_results = []
total_test_time = 0

# 2 раза по 5 запросов
results, test_time = run_stress_test(10, 5)
final_results.extend(results)
total_test_time += test_time

# 2 раза по 25 запросов
# results, test_time = run_stress_test(25, 2)
# final_results.extend(results)
# total_test_time += test_time

# Преобразуем в DataFrame и выводим результаты
df = pd.DataFrame(final_results)

# Выводим результаты в консоль
print(df.to_string())

# Если хочешь сохранить в CSV-файл
df.to_csv("stress_test_results.csv", index=False)

# Итоговое время
print(f"\n⏱ Суммарное время обработки всех тестов: {total_test_time:.4f} сек")
