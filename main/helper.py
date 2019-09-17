def get_given_time(req):
    """
    Return given time of corresponding test.
        Job             | given time
        ----------------|--------------
        Dev             | 3 hours
        Full-time Res   | 3 hours
        part-time Res   | 2 hours
        Do project      | 5 days

    :param req: A main.models.TestRequest object
    :return '5 days', '3 hours' or '2 hours'
    :rtype str
    """
    given_time = "5 days"
    if req.application.is_role_dev() or req.application.is_role_researcher():
        given_time = "3 hours"

    if req.application.is_role_researcher() and req.application.is_intern:
        given_time = "2 hours"

    return given_time
