global_init(input())
session = create_session()
teamleads = []
biggest_command = 0
for user in session.query(User).filter(User.address == 'module_1', User.age < 21).all():
    user.address = 'module_3'
session.commit()
