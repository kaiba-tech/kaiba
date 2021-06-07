from typing_extensions import Final

# Casting
INTEGER_CONTAINING_DECIMALS: Final[str] = 'integer_containing_decimals'
YMD_DATE_FORMAT: Final = r'(^(yy|yyyy)[^\w]?mm[^\w]?dd$)'
DMY_DATE_FORMAT: Final = r'(^dd[^\w]?mm[^\w]?(yy|yyyy)$)'
MDY_DATE_FORMAT: Final = r'(^mm[^\w]?dd[^\w]?(yy|yyyy)$)'

# Casting helpers
COMMA: Final[str] = ','
PERIOD: Final[str] = '.'
EMPTY: Final[str] = ''

# ISO
NAME: Final[str] = 'name'
ALPHA_TWO: Final[str] = 'alpha_2'
ALPHA_THREE: Final[str] = 'alpha_3'
NUMERIC: Final[str] = 'numeric'
OFFICIAL_NAME: Final[str] = 'official_name'
INVALID: Final[str] = 'invalid'
