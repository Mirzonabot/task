from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import smtplib

# Initialize Database
Base = declarative_base()
engine = create_engine('sqlite:///office_rooms.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define Models
class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True, nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    room = relationship("Room", backref="reservations")
    user = relationship("User", backref="reservations")

Base.metadata.create_all(engine)

# Function to check room availability
def check_availability(room_id, check_time):
    reservation = session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.start_time <= check_time,
        Reservation.end_time >= check_time
    ).first()
    if reservation:
        print(f"Room is busy by {reservation.user.name} from {reservation.start_time} to {reservation.end_time}.")
    else:
        print("Room is available.")

# Function to reserve room
def reserve_room(room_id, user_id, start_time, end_time):
    existing_reservation = session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).first()
    if existing_reservation:
        print(f"Room is already reserved by {existing_reservation.user.name} until {existing_reservation.end_time}.")
    else:
        new_reservation = Reservation(room_id=room_id, user_id=user_id, start_time=start_time, end_time=end_time)
        session.add(new_reservation)
        session.commit()
        send_notification(user_id, room_id, start_time)
        print("Room reserved successfully.")

# Placeholder for sending notifications
def send_notification(user_id, room_id, reservation_time):
    user = session.query(User).get(user_id)
    # Email and SMS logic
    print(f"Notification sent to {user.name} ({user.email}, {user.phone}) for room {room_id} reserved at {reservation_time}.")

# Example Usage
check_availability(room_id=1, check_time=datetime(2024, 10, 31, 10, 0))
reserve_room(room_id=1, user_id=2, start_time=datetime(2024, 10, 31, 10, 0), end_time=datetime(2024, 10, 31, 12, 0))
