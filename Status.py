from enum import Enum, unique


__author__ = 'propbono'

@unique
class status(Enum):
    New = 1         # all new uploads
    Prepped = 2     # all uploads prepared for plating - G
    InApproval = 3  # all uploads sent for approval and waiting
    OnHold = 4      # all uploads put on hold by any reason
    Cancelled = 5   # all uploads cancelled
    PressReady = 6  # all uploads in press ready
    Done = 7        # all uploads already on the run
    Sings = 8       # all uploads sent to signs
    Digital = 9     # all uploads sent to digital
    Outsourced = 10   # all uploads outsourced


    @classmethod
    def default(cls):
        return cls.New

    def __str__(self):
        return self.name

