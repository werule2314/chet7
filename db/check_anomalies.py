from models import Term, Definition, Source, get_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

print("🔍 Проверка базы на аномалии:")

# 1. Дубликаты терминов
duplicate_terms = session.query(Term.name, func.count(Term.id)) \
    .group_by(Term.name) \
    .having(func.count(Term.id) > 1).all()

if duplicate_terms:
    print("\n‼️ Найдены дубликаты терминов:")
    for name, count in duplicate_terms:
        print(f"Термин '{name}' встречается {count} раз(а)")
else:
    print("\n✅ Нет дубликатов терминов.")

# 2. Определения без привязки к термину
orphan_definitions = session.query(Definition).filter(Definition.term_id == None).all()

if orphan_definitions:
    print(f"\n‼️ Найдены {len(orphan_definitions)} определений без привязки к термину.")
else:
    print("\n✅ Все определения привязаны к терминам.")

# 3. Термины без источников
terms_without_sources = session.query(Term).filter(~Term.sources.any()).all()

if terms_without_sources:
    print(f"\n⚠️ Термины без источников: {[t.name for t in terms_without_sources]}")
else:
    print("\n✅ Все термины имеют источники.")

# 4. Источники без терминов
sources_without_terms = session.query(Source).filter(~Source.terms.any()).all()

if sources_without_terms:
    print(f"\n⚠️ Источники без терминов: {[s.title for s in sources_without_terms]}")
else:
    print("\n✅ Все источники привязаны к терминам.")

session.close()
