global_init(input())
session = create_session()
teamleads = set()
biggest_command = 0
for job in session.query(Jobs).all():
    size = len(job.collaborators.split(', '))
    if size >= biggest_command:
        if size > biggest_command:
            teamleads = set()
            biggest_command = size
        teamlead = session.query(User).filter(User.id == job.team_leader).first()
        teamleads.add(f'{teamlead.name} {teamlead.surname}')

print("\n".join(teamleads))
