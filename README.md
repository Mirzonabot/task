# Office Room Reservation System

A command-line interface (CLI) application for managing office room reservations.

## Features

- Add and manage rooms
- Add and manage users
- Check room availability
- Make room reservations
- Automatic notification system
- SQLite database storage

## Installation

1. Clone the repository: 

```
git clone <repository-url>
cd office-rooms
```

2. Create a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

To start the application:
```
python -m office_rooms.main
```
### Available Commands

1. **Add a Room**
```
add_room <room_number>
```
Example: add_room 101

2. **Add a User**
```
add_user <name> <email> <phone>
```
Example: add_user JohnDoe john@example.com 1234567890

3. **Check Room Availability**
```
check <room_id> <date> <time>
```
Example: check 1 2024-03-20 14:30

4. **Make a Reservation**
```
reserve <room_id> <user_id> <start_date> <start_time> <end_date> <end_time>
```
Example: reserve 1 1 2024-03-20 14:30 2024-03-20 16:30

5. **List All Rooms**
```
list_rooms
```
6. **List All Users**
```
list_users
```

7. **Exit the Program**
```
quit
```

### Reservation Rules

- Reservations cannot be made in the past
- End time must be after start time
- Maximum reservation duration is 24 hours
- Rooms cannot be double-booked
- Date and time format must be: YYYY-MM-DD HH:MM

## Database

The system uses SQLite database (office_rooms.db) which is automatically created in the project directory when the application runs for the first time.

## Requirements

See requirements.txt for detailed dependencies. Main requirements include:
- Python 3.7+
- SQLAlchemy
- Other dependencies as listed in requirements.txt

## Error Handling

The system provides clear error messages for:
- Invalid date/time formats
- Double bookings
- Past date reservations
- Invalid room or user IDs
- Missing or incorrect command arguments

## Example Session

(reservation) add_room 101
Room 101 added successfully.
(reservation) add_user JohnDoe john@example.com 555-0123
User JohnDoe added successfully.
(reservation) list_rooms
Room ID: 1, Number: 101
(reservation) reserve 1 1 2024-03-20 14:30 2024-03-20 16:30
Room reserved successfully.
Notification sent to JohnDoe (john@example.com, 555-0123)
office_rooms/
├── init.py
├── main.py # Main CLI interface
├── models.py # Database models
├── database.py # Database connection
├── reservations.py # Reservation logic
└── notifications.py # Notification system
For the requirements.txt file:
requirements.txt
This README provides a comprehensive guide for users to understand and use the system effectively. The documentation includes installation instructions, usage examples, and clear explanations of all available commands and features.