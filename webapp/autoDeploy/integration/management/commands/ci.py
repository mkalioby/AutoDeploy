from django.core.management.base import BaseCommand
from django.conf import settings
import os
from integration.models import CIProject
from autoDeploy.api import integrate_core
from django.utils import timezone
from autodeploy_client import Client

CI_CHECK_PATH = settings.CI_CHECK_PATH


def savePID():
    f = open(CI_CHECK_PATH, "w")
    f.write(str(os.getpid()))
    f.close()


def getPreviousPID():
    if not os.path.exists(CI_CHECK_PATH): return 0
    f = open(CI_CHECK_PATH, "r")
    return int(f.read().strip())


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def send_integration_request(server, project, tag=None, commit=None):
    print("integrate_core => ", server, project, commit, tag)
    integrate_core(server, project, tag, commit)


class Command(BaseCommand):
    help = 'continuous integration pulling'

    def add_arguments(self, parser):
        parser.add_argument("--execute", action="store_true", default=True)
        parser.add_argument('--id', nargs='?', type=str, default=None)

    def handle(self, *args, **options):
        pid = getPreviousPID()
        if pid != 0:
            if check_pid(pid):
                print("Another check is running, exiting....")
                exit(-13)
        savePID()
        if options.get('id', None):
            projects = CIProject.objects.filter(id__in=[id for id in options['id'].split(";")])
        else:
            projects = CIProject.objects.all()
        for project in projects:
            updateRequired = False
            print("Checking %s on %s" % (project.name, project.default_server.DNS))
            c = Client(str(project.repo_type), project.default_server.ip, project.default_server.port,project.sshKey.key)
            c.Pull(project.repo, project.working_dir, project.sshKey.key)
            if project.update_style == "commit":
                commits = c.ListCommits(project.working_dir)
                last_commit = commits[0]["Hash"]
                if project.lastCommit != commits[0]["Hash"]:
                    updateRequired = True
                    if options['execute']: send_integration_request(project.default_server, project, commit=last_commit)
                    project.lastCommit = last_commit
            else:
                tags = c.ListTags(project.working_dir)
                if len(tags) > 0:
                    last_tag = tags[0]["Tag"]
                    if project.lastTag != last_tag:
                        updateRequired = True
                        if options['execute']: send_integration_request(project.default_server, project, tag=last_tag)
                        project.lastTag = last_tag
                else:
                    print("No Tags Found")

            if updateRequired:
                project.lastUpdate = timezone.now()
                project.newVersion = True
                project.save()
                print("Update Required")
            else:
                print("Already up-to-date.")
