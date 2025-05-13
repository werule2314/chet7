import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from sqlalchemy.orm import sessionmaker
from db.models import Term, Definition, Source, get_engine
from utils.security import encrypt_text, decrypt_text
from cryptography.fernet import InvalidToken


st.set_page_config(page_title="chet7 — Система учёта терминов", layout="wide")

engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

st.markdown("<h1 style='color:#3c75c0;'>🛡 chet7 — Учёт терминов и определений</h1>", unsafe_allow_html=True)

menu = st.radio("📌 Навигация по разделам:", [
    "🏠 Главная",
    "➕ Добавить",
    "📖 Просмотр",
    "🔎 Поиск",
    "🗑 Удаление"
], horizontal=True)

st.markdown("---")

# === Главная
if menu == "🏠 Главная":
    st.info("🎓 Этот проект создан в рамках выпускной квалификационной работы по направлению 'Информационная безопасность'.")
    st.markdown("""
    **Возможности системы**:
    - 🗂 Добавление терминов, определений и источников
    - 🔐 Шифрование всех определений (алгоритм Fernet)
    - 🔍 Поиск по терминам и содержанию
    - 🧹 Удаление с подтверждением
    - 📚 Привязка источников к терминам

    **Используемые технологии**:
    `Streamlit`, `PostgreSQL`, `SQLAlchemy`, `cryptography`, `dotenv`
    """)

# === Добавить
elif menu == "➕ Добавить":
    st.markdown("### ➕ Добавление термина")
    with st.form("add_term_form"):
        name = st.text_input("📘 Название термина")
        definition = st.text_area("📝 Определение")
        source_title = st.text_input("🔗 Источник (название)")
        source_year = st.number_input("📅 Год публикации", 1900, 2100, 2024)
        submitted = st.form_submit_button("💾 Сохранить термин")

        if submitted:
            if not name or not definition or not source_title:
                st.warning("⚠️ Заполните все поля.")
            elif session.query(Term).filter_by(name=name).first():
                st.error("🚫 Такой термин уже существует.")
            else:
                term = Term(name=name)
                encrypted = encrypt_text(definition)
                term.definitions.append(Definition(content=encrypted))

                source = session.query(Source).filter_by(title=source_title, year=source_year).first()
                if not source:
                    source = Source(title=source_title, year=source_year)

                term.sources.append(source)
                session.add(term)
                session.commit()
                st.success(f"✅ Термин **{name}** добавлен в базу.")

# === Просмотр
elif menu == "📖 Просмотр":
    st.markdown("### 📖 Все термины")
    terms = session.query(Term).all()
    if not terms:
        st.info("Нет данных.")
    for t in terms:
        with st.expander(f"📘 {t.name}", expanded=False):
            for d in t.definitions:
                try:
                    st.markdown(f"📝 _{decrypt_text(d.content)}_")
                except:
                    st.markdown("❌ Не удалось расшифровать")
            for s in t.sources:
                st.markdown(f"🔗 **Источник**: `{s.title}` ({s.year})")
        st.divider()

# === Поиск
elif menu == "🔎 Поиск":
    st.markdown("### 🔍 Поиск по базе")
    col1, col2 = st.columns(2)

    with col1:
        search_term = st.text_input("🔤 Поиск по названию термина")
        if st.button("Найти термин"):
            results = session.query(Term).filter(Term.name.ilike(f"%{search_term}%")).all()
            if not results:
                st.warning("❌ Термины не найдены.")
            for t in results:
                with st.expander(f"📘 {t.name}"):
                    for d in t.definitions:
                        try:
                            st.markdown(f"- _{decrypt_text(d.content)}_")
                        except:
                            st.markdown("- ❌ Не удалось расшифровать")

    with col2:
        keyword = st.text_input("🔤 Поиск по содержанию определения")
        if st.button("Найти определение"):
            defs = session.query(Definition).all()
            found = False
            for d in defs:
                try:
                    text = decrypt_text(d.content)
                    if keyword.lower() in text.lower():
                        st.success(f"📘 **{d.term.name}** → {text}")
                        found = True
                except:
                    continue
            if not found:
                st.info("Нет совпадений.")

# === Удаление
elif menu == "🗑 Удаление":
    st.markdown("### 🗑 Удаление термина")
    terms = session.query(Term).all()
    if not terms:
        st.info("Нет терминов для удаления.")
    else:
        selected = st.selectbox("Выберите термин для удаления", [t.name for t in terms])
        confirm = st.checkbox("Подтверждаю удаление термина")

        if st.button("❌ Удалить термин"):
            if not confirm:
                st.warning("Вы должны подтвердить удаление.")
            else:
                term = session.query(Term).filter_by(name=selected).first()
                session.delete(term)
                session.commit()
                st.success(f"✅ Термин **{selected}** успешно удалён.")
