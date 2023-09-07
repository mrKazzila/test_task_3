import logging

from project_data_types import Domain

logger = logging.getLogger(__name__)


def _create_list_with_domains(project_domains: list[Domain]) -> list[str]:
    return [domain.domain for domain in project_domains]


def _generate_regexp_pattern_for_project_domains(domains: list[str]) -> str:
    trash_patterns = []

    for domain in domains:
        subdomains = domain.split('.')

        if len(subdomains) >= 3:
            if len(subdomains) >= 4:
                trash_pattern = r'\.'.join(subdomains[:-2]) + r'\.\w+\.\w+'
            else:
                trash_pattern = r'\.' + r'\.'.join(subdomains[:-2]) + r'\.\w+\.\w+'

            logger.debug(f'{domain=} || domains lvl={len(subdomains)} || regex={trash_pattern}')
            trash_patterns.append(trash_pattern)

    return '|'.join(trash_patterns) if trash_patterns else ''
