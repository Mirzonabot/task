from datetime import datetime
import cmd
from .database import get_db_session
from .models import Base, Room, User
from .reservations import ReservationManager

class RoomReservationShell(cmd.Cmd):
    intro = 'Welcome to the Room Reservation System. Type help or ? to list commands.\n'
    prompt = '(reservation) '

    def __init__(self):
        super().__init__()
        self.session = get_db_session()
        self.reservation_manager = ReservationManager()
        
        # Create tables if they don't exist
        engine = self.session.get_bind()
        Base.metadata.create_all(engine)

    def do_add_room(self, arg):
        """Add a new room: add_room <room_number>"""
        try:
            room = Room(room_number=arg)
            self.session.add(room)
            self.session.commit()
            print(f"Room {arg} added successfully.")
        except Exception as e:
            print(f"Error adding room: {e}")

    def do_add_user(self, arg):
        """Add a new user: add_user <name> <email> <phone>"""
        try:
            name, email, phone = arg.split()
            user = User(name=name, email=email, phone=phone)
            self.session.add(user)
            self.session.commit()
            print(f"User {name} added successfully.")
        except Exception as e:
            print(f"Error adding user: {e}")

    def do_check(self, arg):
        """Check room availability: check <room_id> <YYYY-MM-DD HH:MM>"""
        try:
            room_id, date_str = arg.split(' ', 1)
            check_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            available, message = self.reservation_manager.check_availability(int(room_id), check_time)
            print(message)
        except Exception as e:
            print(f"Error checking availability: {e}")

    def do_reserve(self, arg):
        """Reserve a room: reserve <room_id> <user_id> <start_time> <end_time>
        Time format: YYYY-MM-DD HH:MM
        Example: reserve 1 1 2024-03-20 14:30 2024-03-20 16:30"""
        try:
            # First, normalize spaces and split
            args = ' '.join(arg.split()).split()
            
            # Check minimum required parts (room_id, user_id, and at least some datetime info)
            if len(args) < 4:
                print("Error: Not enough arguments")
                self._show_reserve_help()
                return

            # Extract room_id and user_id
            room_id, user_id = args[0:2]
            datetime_parts = args[2:]  # Rest of the arguments are for datetime
            print("datetime parts: " + str(datetime_parts))
            
            try:
                # Join the remaining parts and attempt to split into start and end times
                datetime_str = ' '.join(datetime_parts)
                
                parts = datetime_str.split()
                start_str = f"{parts[0]} {parts[1]}"
                end_str = f"{parts[2]} {parts[3]}"
                
                # Validate room_id and user_id are integers
                room_id = int(room_id)
                user_id = int(user_id)
                
                # Parse dates
                start_time = datetime.strptime(start_str, '%Y-%m-%d %H:%M')
                end_time = datetime.strptime(end_str, '%Y-%m-%d %H:%M')
                
            except ValueError as ve:
                print("Error: Invalid format")
                print("Correct format: reserve <room_id> <user_id> <YYYY-MM-DD HH:MM> <YYYY-MM-DD HH:MM>")
                print("Example: reserve 1 1 2024-03-20 14:30 2024-03-20 16:30")
                return
            
            # Validate dates
            current_time = datetime.now()
            if start_time < current_time:
                print("Error: Start time cannot be in the past")
                return
            
            if end_time <= start_time:
                print("Error: End time must be after start time")
                return
            
            # Calculate duration in hours
            duration = (end_time - start_time).total_seconds() / 3600
            if duration > 24:
                print("Error: Reservation cannot exceed 24 hours")
                return
            
            # Proceed with reservation
            success, message = self.reservation_manager.reserve_room(
                room_id, user_id, start_time, end_time
            )
            print(message)
            
        except Exception as e:
            print(f"Error making reservation: {str(e)}")
            self._show_reserve_help()
    def do_list_rooms(self, arg):
        """List all rooms"""
        rooms = self.session.query(Room).all()
        for room in rooms:
            print(f"Room ID: {room.id}, Number: {room.room_number}")

    def do_list_users(self, arg):
        """List all users"""
        users = self.session.query(User).all()
        for user in users:
            print(f"User ID: {user.id}, Name: {user.name}, Email: {user.email}")

    def do_quit(self, arg):
        """Exit the program"""
        print("Goodbye!")
        return True

if __name__ == '__main__':
    RoomReservationShell().cmdloop() 