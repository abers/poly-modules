import time as t
from datetime import datetime, time

import pyinotify
from tasklib import TaskWarrior

BEGIN_WORK = time(9, 00)
END_WORK = time(17, 00)

TW = TaskWarrior("/home/alasdair/.task")
TASK_FILE = "/home/alasdair/.task/pending.data"


def is_work_hours():
    now = datetime.now().time()
    today = datetime.today().strftime("%A")
    if (
        now > BEGIN_WORK
        and now < END_WORK
        and today != "Saturday"
        and today != "Sunday"
    ):
        return True
    else:
        return False


class Tasks:
    def __init__(self):
        self.tasks = TW.tasks.pending()
        self.active = self.tasks.filter("+ACTIVE")
        self.urgent_work = self.tasks.filter("+Urgent", project="work")
        self.overdue_work = self.tasks.filter("+OVERDUE", project="work")
        self.urgent_personal = self.tasks.filter("+Urgent", project="personal")
        self.overdue_personal = self.tasks.filter(
            "+OVERDUE", project="personal"
        )
        self.any_active_urgent()
        print(self.label)

    def format_task_label(self, task, additional=None):
        self.label = f"Task {task[0]['id']}: {task[0]}"
        if additional:
            self.label = self.label + f" {additional}"

    def any_active_urgent(self):
        if self.active:
            self.format_task_label(self.active, additional="(active)")
        elif self.overdue_work and is_work_hours():
            self.format_task_label(self.overdue_work, additional="(overdue)")
        elif self.urgent_work and is_work_hours():
            self.format_task_label(self.urgent_work, additional="(urgent)")
        elif self.overdue_personal and not is_work_hours():
            self.format_task_label(
                self.overdue_personal, additional="(overdue)"
            )
        elif self.urgent_personal and not is_work_hours():
            self.format_task_label(self.urgent_personal, additional="(urgent)")
        else:
            self.label = ""


class FileModHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        global wf
        wm.rm_watch(wf["/home/alasdair/.task/pending.data"])
        t.sleep(1)
        tasks.__init__()
        wf = wm.add_watch("/home/alasdair/.task/pending.data", mask)


tasks = Tasks()

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CLOSE_WRITE
notifier = pyinotify.ThreadedNotifier(wm, FileModHandler(), timeout=10)
notifier.start()

wf = wm.add_watch("/home/alasdair/.task/pending.data", mask)
