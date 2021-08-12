from .models import OpenJob


def get_given_time(req):
    given_time = None
    try:
        app = req.application
        open_job = OpenJob.objects.get(position=app.position, typ=app.typ, workplace=app.workplace)
        given_time = open_job.test_duration
    except Exception:
        pass

    return given_time
