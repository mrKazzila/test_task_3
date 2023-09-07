import re
from collections import namedtuple

import pytest

from helpers import _generate_regexp_pattern_for_project_domains

case = namedtuple('TestCase', 'domain, result')

test_cases = [
    case(domain='sub.yyy.com', result=False),
    case(domain='autodiscover.xxx.com', result=False),
    case(domain='smartapp-code.xxx.com', result=False),
    case(domain='auth.fine.xxx.com', result=True),
    case(domain='canvas.hs-beta.xxx.com', result=True),
    case(domain='9hdfdrv3os1j.sub.yyy.com', result=True),
    case(domain='killbill.smartpay.xxx.com', result=True),
    case(domain='foodtech.strapi.prom.fine.xxx.com', result=True),
    case(domain='f1cbed24-ac53-46d6-be04-4ae47f8d398a.static.developer.xxx.com', result=True),
]


@pytest.mark.parametrize('domain, expected_result', test_cases)
def test_positive_generate_regexp_pattern_for_project_domains(domain, expected_result):
    pattern = _generate_regexp_pattern_for_project_domains(domains=[domain])
    result = True if re.search(pattern, domain) is not None else False

    assert result == expected_result
