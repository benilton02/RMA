from enum import Enum

class RMAStatusEnum(str, Enum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    FINISHED = "FINISHED"
    TESTING = "TESTING"
    REPAIR = "REPAIR"
    REPLACEMENT = "REPLACEMENT"
    REFUND = "REFUND"    

 
class RolesEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"