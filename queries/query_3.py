global_init(input())
session = create_session()
for user in session.query(User).filter(User.age < 18).all():
    print(str(user) + f" {user.age} years")
