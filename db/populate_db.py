from db.models import Term, Definition, Source, get_engine, Base
from sqlalchemy.orm import sessionmaker
from utils.security import encrypt_text
from dotenv import load_dotenv
import random
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


load_dotenv()

engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

# Очистка и пересоздание базы
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Источники
sources = [
    Source(title="ГОСТ 1234-56", year=2019),
    Source(title="Словарь по ИБ", year=2020),
    Source(title="Методические рекомендации ФСТЭК", year=2021),
    Source(title="ISO/IEC 27001", year=2018),
    Source(title="Учебник по ИБ, Том I", year=2022)
]

# Термины и определения
terms_data = {
    "Конфиденциальность": [
        "Свойство информации быть доступной только авторизованным субъектам.",
        "Ограничение доступа к информации посторонним лицам."
    ],
    "Аутентификация": [
        "Проверка подлинности пользователя с помощью пароля или сертификата."
    ],
    "Целостность": [
        "Сохранение неизменности данных.",
        "Защита информации от несанкционированных изменений."
    ],
    "Доступность": [
        "Обеспечение возможности доступа к информации в нужное время."
    ],
    "Несанкционированный доступ": [
        "Доступ к ресурсам без прав или разрешения."
    ],
    "Криптография": [
        "Наука о методах защиты информации с использованием шифрования."
    ],
    "Симметричное шифрование": [
        "Метод шифрования, при котором один и тот же ключ используется для шифрования и расшифровки."
    ],
    "Асимметричное шифрование": [
        "Использование пары ключей: открытого и закрытого для шифрования и расшифровки."
    ],
    "Цифровая подпись": [
        "Механизм проверки подлинности и целостности электронного документа."
    ],
    "Информационная безопасность": [
        "Состояние защищённости информационной среды от внутренних и внешних угроз."
    ]
}

# Добавление в базу
for term_name, definitions in terms_data.items():
    term = Term(name=term_name)
    for definition in definitions:
        encrypted = encrypt_text(definition)
        term.definitions.append(Definition(content=encrypted))

    # случайно привяжем 1–3 источника
    term.sources.extend(random.sample(sources, k=random.randint(1, 3)))
    session.add(term)

session.add_all(sources)
session.commit()
session.close()

print("✅ База насыщена расширенным списком зашифрованных терминов.")
