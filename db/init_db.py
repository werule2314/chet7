from models import Base, get_engine

def init_db():
    engine = get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("База данных создана.")
