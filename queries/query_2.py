global_init(input())
session = create_session()
for user in session.query(User).filter(
        User.address == 'module_1',
        User.speciality.notlike('%ingeneer%'),
        User.position.notlike('%ingeneer%')
).all():
    print(user.id)
