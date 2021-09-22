import enum


class ApplicationStatus2021(enum.Enum):
    NEW = 'New'
    FAILED = 'Failed'
    INVITE_SENT = 'Invite_Sent'
    INVITE_ACCEPTED = 'Invite_Accepted'
    INVITE_REFUSED = 'Invite_Refused'
    REMINDER_1_SENT = 'Reminder_1_Sent'
    REMINDER_2_SENT = 'Reminder_2_Sent'
