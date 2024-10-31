from datetime import datetime
from .database import get_db_session
from .models import Reservation, Room, User
from .notifications import send_notification

class ReservationManager:
    def __init__(self):
        self.session = get_db_session()

    def check_availability(self, room_id, check_time):
        reservation = self.session.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.start_time <= check_time,
            Reservation.end_time >= check_time
        ).first()
        
        if reservation:
            return False, f"Room is busy by {reservation.user.name} from {reservation.start_time} to {reservation.end_time}."
        return True, "Room is available."

    def reserve_room(self, room_id, user_id, start_time, end_time):
        existing_reservation = self.session.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        ).first()
        
        if existing_reservation:
            return False, f"Room is already reserved by {existing_reservation.user.name} until {existing_reservation.end_time}."
        
        try:
            new_reservation = Reservation(
                room_id=room_id,
                user_id=user_id,
                start_time=start_time,
                end_time=end_time
            )
            self.session.add(new_reservation)
            self.session.commit()
            
            user = self.session.query(User).get(user_id)
            room = self.session.query(Room).get(room_id)
            send_notification(user, room, start_time)
            
            return True, "Room reserved successfully."
        except Exception as e:
            self.session.rollback()
            return False, f"Error reserving room: {str(e)}" 