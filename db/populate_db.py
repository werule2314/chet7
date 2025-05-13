from db.models import Term, Definition, Source, get_engine, Base
from sqlalchemy.orm import sessionmaker
from utils.security import encrypt_text
import os
from dotenv import load_dotenv

load_dotenv()

# Создание подключения и сессии
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

# Очистка и пересоздание базы
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Источники
source1 = Source(title="Словарь по информационной безопасности", year=2020)
source2 = Source(title="ГОСТ 1234-56", year=2019)

# Шифруем определения
def1 = encrypt_text("Свойство информации быть доступной только авторизованным субъектам.")
def2 = encrypt_text("Процесс проверки подлинности субъекта с использованием учётных данных.")
def3 = encrypt_text("Свойство информации сохранять неизменность и защищённость от изменений.")

# Термины
term1 = Term(name="Конфиденциальность")
term1.definitions.append(Definition(content=def1))
term1.sources.extend([source1, source2])

term2 = Term(name="Аутентификация")
term2.definitions.append(Definition(content=def2))
term2.sources.append(source1)

term3 = Term(name="Целостность")
term3.definitions.append(Definition(content=def3))
term3.sources.append(source2)

# Добавляем в базу
session.add_all([term1, term2, term3])
session.commit()
session.close()

print("✅ База успешно заполнена зашифрованными терминами.")
