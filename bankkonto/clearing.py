"""
:mod:`clearing`
=======================

List of clearing numbers fetched from `Swedish Bankers'
Association <http://www.swedishbankers.se/fraagor-vi-arbetar-med/clearingnummer/clearingnummer/>`_.

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>
Created on 2017-02-15, 11:13

"""

import re
from typing import Tuple

from .exceptions import BankkontoException

_CLEARING_LIST = """
Sveriges Riksbank 1000-1099
Nordea 1100-1199
Danske Bank 1200-1399
Nordea 1400-2099
Ålandsbanken Sverige AB 2300-2399
Danske Bank 2400-2499
Nordea (exkl. personkonton, cl 3300) 3000-3399
Nordea Personkonto 3300
Länsförsäkringar Bank 3400-3409
Nordea (exkl. personkonton, cl 3782) 3410-3999
Nordea Personkonto 3782
Nordea 4000-4999
SEB 5000-5999
Handelsbanken 6000-6999
Swedbank 7000-7999
Swedbank 8000-8999
Länsförsäkringar Bank 9020-9029
Citibank 9040-9049
Länsförsäkringar Bank 9060-9069
Multitude Bank plc 9070-9079
Nordnet Bank 9100-9109
SEB 9120-9124
SEB 9130-9149
Skandiabanken 9150-9169
Ikano Bank 9170-9179
Danske Bank 9180-9189
DNB Bank 9190-9199
Marginalen Bank 9230-9239
SBAB 9250-9259
DNB Bank 9260-9269
ICA Banken AB 9270-9279
Resurs Bank 9280-9289
Swedbank 9300-9349
Landshypotek Bank 9390-9399
Santander Consumer Bank AS 9460-9469
BNP Paribas SA 9470-9479
Avanza Bank AB 9550-9569
Aion Bank SA 9580-9589
Erik Penser AB 9590-9599
Volvofinans Bank 9610-9619
Bank of China (Luxembourg) 9620-9629
Lån & Spar Bank Sverige 9630-9639
NOBA Bank Group AB 9640-9649
Svea Bank AB 9660-9669
JAK Medlemsbank 9670-9679
Bluestep Finans AB 9680-9689
Lunar Bank A/S 9710-9719
Ekobanken 9700-9709
Northmill Bank AB 9750-9759
Klarna Bank 9780-9789
Riksgälden 9880-9889
Nordea (Plusgirot) 9960-9969
"""


clearing_nbrs = [
    (_parse_result[0], int(_parse_result[1]), int(_parse_result[2]) if _parse_result[2] else int(_parse_result[1]))
    for _parse_result in re.findall("(.+)\\s([\\d]+)-*(\\d*)", _CLEARING_LIST.strip())
]
clearing_nbrs.sort(key=lambda x: x[1])


def get_bank_from_clearing_number(nbr: str | int) -> str:
    nbr = int(nbr)

    if nbr < 1000 or nbr > 9999:
        raise BankkontoException("Clearing number must be in range 1000 - 9999.")
    res = list(filter(lambda x: nbr >= x[1] and nbr <= x[2], clearing_nbrs))
    if len(res) == 0:
        raise BankkontoException("Clearing number {0} does not correspond to any Swedish bank.")
    else:
        bank = res[0][0]
        assert isinstance(bank, str)
        return bank


def get_clearing_ranges_for_bank(bank: str) -> Tuple[Tuple[int, ...], ...]:
    res = list(filter(lambda x: x[0] == bank, clearing_nbrs))
    if len(res) == 0:
        raise BankkontoException("Incorrect bank name.")
    else:
        return tuple(tuple(x[1:]) for x in res)
