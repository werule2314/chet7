from models import Term, Definition, Source, get_engine, Base
from sqlalchemy.orm import sessionmaker

# Настройка сессии
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

# Удалим всё старое (для тестов)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Источники
source1 = Source(title="Словарь по информационной безопасности", year=2020)
source2 = Source(title="ГОСТ 1234-56", year=2019)

# Термины и определения
term1 = Term(name="Конфиденциальность")
term1.definitions.append(Definition(content="Свойство информации быть доступной только авторизованным субъектам."))
term1.sources.extend([source1, source2])

term2 = Term(name="Аутентификация")
term2.definitions.append(Definition(content="Процесс проверки подлинности субъекта с использованием учётных данных."))
term2.sources.append(source1)

term3 = Term(name="Целостность")
term3.definitions.append(Definition(content="Свойство информации сохранять неизменность и защищенность от несанкционированного изменения."))
term3.sources.append(source2)

# Добавляем в сессию и сохраняем
session.add_all([term1, term2, term3])
session.commit()
session.close()

print("База успешно заполнена тестовыми данными.")
