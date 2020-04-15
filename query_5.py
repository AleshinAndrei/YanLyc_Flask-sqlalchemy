class Jobs(Jobs):
    def _repr_(self):
        return f"<Job> {self.job}"


global_init(input())
session = create_session()
for job in session.query(Jobs).filter(
    Jobs.work_size < 20,
    Jobs.is_finished == 0
).all():
    print(job)
