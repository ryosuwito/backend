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

    POSITION_CHOICES = (
        (DEVELOPER, "Developer"),
        (DATA_ENGINEER, "Data Engineer"),
        (OPERATION_SPECIALIST, "Trading Support Engineer"),
        (Q_RESEARCHER, "Quantitative Researcher"),
        (FQ_RESEARCHER, "Fundamental Quantitative Researcher"),
    )

    INTERN_POSITION_CHOICES = (
        (INTERN_Q_RESEARCHER, "Quantitative Researcher (Internship)"),
        (INTERN_FQ_RESEARCHER, "Fundamental Quantitative Researcher (Internship)"),
        (INTERN_DEVELOPER, "Developer (Internship)"),
        (INTERN_DATA_ENGINEER, "Data Engineer (Internship)"),
    )


class JobPosition(enum.Enum):
    """
    After 2019.08.29
    """
    FSDEV = "Full-Stack Developer"
    DEV = "Developer"
    DATA_ENGINEER = "Data Engineer"
    OP_SPECIALIST = "Trading Support Engineer"
    QRES = "Quantitative Researcher"
    FQRES = "Fundamental Quantitative Researcher"
    SYSAD = "System Administrator"
    # DATA_ANALYST = "Data Analyst"
    FPGA_ENGINEER = "FPGA Engineer"


class JobType(enum.Enum):
    FULLTIME_INTERNSHIP = 'Full-time Internship'
    PARTTIME_INTERNSHIP = 'Part-time Internship'
    FULLTIME_JOB = 'Full-time'
    INTERNSHIP = 'Internship'


class Workplace(enum.Enum):
    SHANGHAI = 'Shanghai'
    SINGAPORE = 'Singapore'
    REMOTE = 'Remote'


JobTypeChoices = [(typ.name, typ.value) for typ in JobType]
JobWorkplaceChoices = [(place.name, place.value) for place in Workplace]
JobPositionChoices = [(pos.name, pos.value) for pos in JobPosition]
