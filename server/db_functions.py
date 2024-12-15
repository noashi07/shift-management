import database
def add_user(name, password):
    session = database.Session()
    new_user = database.User(name=name, password=password)
    session.add(new_user)
    session.commit()
    session.close()


def get_all_users():
    session = database.Session()
    users = session.query(database.User).all()  # Retrieves all users
    session.close()
    return users

def user_exists(name):
    session = database.Session()
    user = session.query(database.User).filter_by(name=name).first()  # Checks if the user exists
    session.close()
    return user is not None  # Returns True if user exists, False otherwise


# Add a user
# add_user("noanoa", "asdfghjk")

# # Check if a user exists
# if user_exists("john_doe"):
#     print("User exists")
# else:
#     print("User does not exist")

# Retrieve all users
users = get_all_users()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Password: {user.password}")
