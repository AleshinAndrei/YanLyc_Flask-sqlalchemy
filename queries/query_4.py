global_init(input())
session = create_session()
for user in session.query(User).filter((
        User.position.like("%chief%") | User.position.like("%middle%")
)).all():
    print(str(user) + f" {user.position}")
