from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class StateCode(str, Enum):
    """Valid US state and territory codes"""
    AK = "AK"  # Alaska
    AL = "AL"  # Alabama
    AR = "AR"  # Arkansas
    AZ = "AZ"  # Arizona
    CA = "CA"  # California
    CO = "CO"  # Colorado
    CT = "CT"  # Connecticut
    DC = "DC"  # District of Columbia
    DE = "DE"  # Delaware
    FL = "FL"  # Florida
    GA = "GA"  # Georgia
    HI = "HI"  # Hawaii
    IA = "IA"  # Iowa
    ID = "ID"  # Idaho
    IL = "IL"  # Illinois
    IN = "IN"  # Indiana
    KS = "KS"  # Kansas
    KY = "KY"  # Kentucky
    LA = "LA"  # Louisiana
    MA = "MA"  # Massachusetts
    MD = "MD"  # Maryland
    ME = "ME"  # Maine
    MH = "MH"  # Marshall Islands
    MI = "MI"  # Michigan
    MN = "MN"  # Minnesota
    MO = "MO"  # Missouri
    MS = "MS"  # Mississippi
    MT = "MT"  # Montana
    NC = "NC"  # North Carolina
    ND = "ND"  # North Dakota
    NE = "NE"  # Nebraska
    NH = "NH"  # New Hampshire
    NJ = "NJ"  # New Jersey
    NM = "NM"  # New Mexico
    NV = "NV"  # Nevada
    NY = "NY"  # New York
    OH = "OH"  # Ohio
    OK = "OK"  # Oklahoma
    OR = "OR"  # Oregon
    PA = "PA"  # Pennsylvania
    RI = "RI"  # Rhode Island
    SC = "SC"  # South Carolina
    SD = "SD"  # South Dakota
    TN = "TN"  # Tennessee
    TX = "TX"  # Texas
    UT = "UT"  # Utah
    VA = "VA"  # Virginia
    VT = "VT"  # Vermont
    WA = "WA"  # Washington
    WI = "WI"  # Wisconsin
    WV = "WV"  # West Virginia
    WY = "WY"  # Wyoming


class RoleId(BaseModel):
    id: str = "DRIVER"


class StateId(BaseModel):
    id: StateCode

    class Config:
        use_enum_values = True


class TerminalId(BaseModel):
    id: str


class CycleCode(str, Enum):
    US_70_8 = "USA 70 hour / 8 day"
    US_60_7 = "USA 60 hour / 7 day"
    CA_80_8 = "California 80 hour / 8 day"
    TX_70_7 = "Texas 70 hour / 7 day"


class CycleId(BaseModel):
    id: CycleCode


class CargoTypeId(BaseModel):
    id: str


class RestartCode(str, Enum):
    H34 = "34 Hour Restart"
    H24 = "24 Hour Restart"


class RestartHoursId(BaseModel):
    id: RestartCode


class RestBreakCode(str, Enum):
    M30 = "30 Minute Rest Break Required"
    M0 = "No Rest Break Required"


class RestBreakId(BaseModel):
    id: RestBreakCode


class HosSettings(BaseModel):
    pcAllowed: bool = True
    ymAllowed: bool = True
    is16hShortHaulExceptionAllowed: bool = False
    exempt: bool = False
    suggestedEventOriginIsDriver: bool = False
    cycle: CycleId
    cargoType: CargoTypeId
    restartHours: RestartHoursId
    restBreak: RestBreakId
    rv: int = 2


class DriverInfo(BaseModel):
    companyDriverId: str = ""
    licenseNumber: str
    licenseState: StateId
    homeTerminal: TerminalId
    hosSettings: HosSettings
    avi: List = []


class OuId(BaseModel):
    id: StateCode  # Also uses state codes

    class Config:
        use_enum_values = True


class TypeId(BaseModel):
    id: str = "User"


class DriverCreateRequest(BaseModel):
    companyId: str
    createdBy: str
    email: str
    firstName: str
    lastName: str
    active: bool = True
    phoneNum: str = ""
    role: RoleId = Field(default_factory=lambda: RoleId(id="DRIVER"))
    extraPermissions: List = []
    driverInfo: DriverInfo
    ou: OuId


class DriverUpdateRequest(BaseModel):
    companyId: Optional[str] = None
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    active: Optional[bool] = None
    phoneNum: Optional[str] = None
    role: Optional[RoleId] = None
    extraPermissions: Optional[List] = None
    driverInfo: Optional[DriverInfo] = None
    ou: Optional[OuId] = None


class DriverResponse(BaseModel):
    _id: str
    _rev: str
    companyId: str
    createdBy: str
    createdAt: int
    email: str
    firstName: str
    lastName: str
    active: bool
    phoneNum: str
    role: RoleId
    extraPermissions: List
    driverInfo: DriverInfo
    ou: OuId
    type: TypeId
    stime: int
    dSTime: int
