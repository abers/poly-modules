from tasklib import TaskWarrior

tw = TaskWarrior("/home/alasdair/.task")
tasks = tw.tasks.pending()

work_overdue = tasks.filter("+OVERDUE", project="work")
personal_overdue = tasks.filter("+OVERDUE", project="personal")

print(f"W: {len(work_overdue)} | P: {len(personal_overdue)}")
