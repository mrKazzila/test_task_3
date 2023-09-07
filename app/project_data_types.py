from typing import NamedTuple


class ProjectID(NamedTuple):
    project_id: str


class Domain(NamedTuple):
    domain: str


class RulesData(NamedTuple):
    project_id: str
    regexp: str
