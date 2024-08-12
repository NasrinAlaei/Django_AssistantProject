from django_cron import CronJobBase,Schedule
from .views import archive_sessions

class ArchiveSessions(CronJobBase):
    RUN_EVERY_MINS = 30
    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'archive_sessions'

    def do(self):
      archive_sessions()

