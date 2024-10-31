def send_notification(user, room, reservation_time):
    """Send notification to user about room reservation"""
    # Email and SMS logic would go here
    print(f"Notification sent to {user.name} ({user.email}, {user.phone})")
    print(f"Room {room.room_number} reserved at {reservation_time}")
