import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from sqlalchemy.orm import sessionmaker
from db.models import Term, Definition, Source, get_engine
from utils.security import encrypt_text, decrypt_text
from cryptography.fernet import InvalidToken

st.set_page_config(page_title="Система учёта терминов", layout="wide")

engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

# ===== Интерфейс =====

st.markdown("# 🛡 chet7 — Система учёта терминов и определений")
st.markdown("Добро пожаловать в защищённую систему учета терминов. Используйте меню ниже для работы.")

# Навигация через кнопки
menu = st.radio("Выберите действие:", [
    "🏠 Главная",
    "➕ Добавить термин",
    "📖 Просмотр терминов",
    "🔎 Поиск и выборки",
    "🗑 Удалить термин"
], horizontal=True)

st.markdown("---")

# === Главная ===
if menu == "🏠 Главная":
    st.subheader("🔐 Описание проекта")
    st.markdown("""
    **Cистема chet7** предназначена для безопасного хранения терминов и определений, связанных с информационной безопасностью.

    ✅ Все определения шифруются при сохранении  
    ✅ Удобный интерфейс для поиска и редактирования  
    ✅ Хранение источников и их связь с терминами  

    ---  
    Начните работу с системой, выбрав действие в меню сверху.
    """)

# === Добавление ===
elif menu == "➕ Добавить термин":
    st.subheader("➕ Добавление нового термина")

    name = st.text_input("Название термина")
    definition = st.text_area("Определение")
    source_title = st.text_input("Источник (название)")
    source_year = st.number_input("Год публикации", min_value=1900, max_value=2100, step=1, value=2024)

    if st.button("Сохранить"):
        if not name or not definition or not source_title:
            st.warning("Пожалуйста, заполните все поля.")
        else:
            existing_term = session.query(Term).filter_by(name=name).first()
            if existing_term:
                st.error("Такой термин уже существует.")
            else:
                try:
                    encrypted = encrypt_text(definition)
                    term = Term(name=name)
                    defn = Definition(content=encrypted)
                    term.definitions.append(defn)

                    source = session.query(Source).filter_by(title=source_title, year=source_year).first()
                    if not source:
                        source = Source(title=source_title, year=source_year)

                    term.sources.append(source)
                    session.add(term)
                    session.commit()
                    st.success(f"Термин '{name}' добавлен.")
                except Exception as e:
                    st.error(f"Ошибка при добавлении: {e}")

# === Просмотр ===
elif menu == "📖 Просмотр терминов":
    st.subheader("📖 Все термины")

    terms = session.query(Term).all()
    if not terms:
        st.info("Нет добавленных терминов.")
    for t in terms:
        st.markdown(f"### 📘 {t.name}")
        for d in t.definitions:
            try:
                text = decrypt_text(d.content)
                st.markdown(f"- _Определение_: {text}")
            except InvalidToken:
                st.markdown(f"- ❌ Не удалось расшифровать")
        for s in t.sources:
            st.markdown(f"📌 Источник: **{s.title}**, {s.year}")
        st.markdown("---")

# === Поиск ===
elif menu == "🔎 Поиск и выборки":
    st.subheader("🔎 Поиск по базе")

    search_term = st.text_input("Введите название термина (полное или часть)")
    if st.button("Найти определения термина"):
        results = session.query(Term).filter(Term.name.ilike(f"%{search_term}%")).all()
        if not results:
            st.warning("Ничего не найдено.")
        else:
            for t in results:
                st.markdown(f"### 📘 {t.name}")
                for d in t.definitions:
                    try:
                        decrypted = decrypt_text(d.content)
                        st.markdown(f"- _{decrypted}_")
                    except:
                        st.markdown("- ❌ Не удалось расшифровать")

    st.markdown("---")

    keyword = st.text_input("Поиск по содержимому определений (ключевое слово)")
    if st.button("Найти по определению"):
        definitions = session.query(Definition).all()
        count = 0
        for d in definitions:
            try:
                text = decrypt_text(d.content)
                if keyword.lower() in text.lower():
                    st.markdown(f"- **{d.term.name}** → {text}")
                    count += 1
            except:
                continue
        if count == 0:
            st.info("Совпадений не найдено.")

    st.markdown("---")

    st.subheader("📚 Источники по термину")
    term_for_sources = st.text_input("Введите точное название термина для получения источников")
    if st.button("Показать источники"):
        term = session.query(Term).filter_by(name=term_for_sources).first()
        if not term:
            st.warning("Такой термин не найден.")
        else:
            st.markdown(f"Источники для термина **{term.name}**:")
            for s in term.sources:
                st.markdown(f"- {s.title} ({s.year})")

# === Удаление ===
elif menu == "🗑 Удалить термин":
    st.subheader("🗑 Удаление термина")

    terms = session.query(Term).all()
    names = [t.name for t in terms]
    if names:
        selected = st.selectbox("Выберите термин для удаления", names)
        if st.button("Удалить"):
            term = session.query(Term).filter_by(name=selected).first()
            if term:
                session.delete(term)
                session.commit()
                st.success(f"Термин '{selected}' удалён.")
            else:
                st.warning("Термин не найден.")
    else:
        st.info("Нет доступных терминов для удаления.")
