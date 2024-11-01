from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_db_session():
    engine = create_engine('sqlite:///office_rooms.db')
    Session = sessionmaker(bind=engine)
    return Session()
