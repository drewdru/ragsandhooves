from enum import Enum

class CompanyUserRoleEnum(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    CUSTOMER = "customer"
