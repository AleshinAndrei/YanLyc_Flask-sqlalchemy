# import global_init, create_session, User


global_init(input())
session = create_session()
for user in session.query(User).filter(User.address == 'module_1').all():
    print(user)
