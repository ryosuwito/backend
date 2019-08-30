import enum


class OldJobPosition(enum.Enum):
    """
    Before 2019.08.29
    """
    DEVELOPER = "DEV"
    DATA_ENGINEER = "DATA_ENGINEER"
    OPERATION_SPECIALIST = "OP_SPECIALIST"
    Q_RESEARCHER = "QRES"
    FQ_RESEARCHER = "FQRES"
    INTERN_FQ_RESEARCHER = "INTERN_FQRES"
    INTERN_Q_RESEARCHER = "INTERN_QRES"
    INTERN_DATA_ENGINEER = "INTERN_DATA_ENGINEER"
    INTERN_DEVELOPER = "INTERN_DEVELOPER"


class JobPosition(enum.Enum):
    """
    After 2019.08.29
    """
    DEV = "Developer"
    DATA_ENGINEER = "Data Engineer"
    OP_SPECIALIST = "Operation Specialist"
    QRES = "Quantitative Researcher"
    FQRES = "Fundamental Quantitative Researcher"


class JobType(enum.Enum):
    FULLTIME_INTERNSHIP = 'Full-time Internship'
    PARTTIME_INTERNSHIP = 'Part-time Internship'
    FULLTIME_JOB = 'Full-time Job'


class Workplace(enum.Enum):
    SHANGHAI = 'Shanghai'
    SINGAPORE = 'Singapore'
    REMOTE = 'Remote'
