import asyncio
import logging

from aiosqlite import Connection

from database import Database
from exceptions import DomainsNotFoundException, ProjectsIDNotFoundException
from helpers import _create_list_with_domains, _generate_regexp_pattern_for_project_domains
from project_data_types import Domain, ProjectID, RulesData
from services import DomainsServices
from settings import DB_PATH

logger = logging.getLogger(__name__)


async def get_unique_projects_id(db: Connection) -> list[ProjectID]:
    if projects_id := await DomainsServices.get_unique_projects_id(db=db):
        return projects_id

    raise ProjectsIDNotFoundException(f'{projects_id=}')


async def get_domains_for_project(db: Connection, project_id: str) -> list[Domain]:
    if domains := await DomainsServices.get_domains_by_project_id(db=db, project_id=project_id):
        return domains

    raise DomainsNotFoundException(f'{domains=}')


async def add_regexp_for_project(db: Connection, regexp: str, project_id: str) -> None:
    await DomainsServices.insert_or_replace_regexp_pattern(
        db=db,
        regexp_pattern=regexp,
        project_id=project_id,
    )


async def create_regex_for_projects(db: Connection, projects: list[ProjectID]) -> list[RulesData]:
    result = []

    for project_id in projects:
        project_domains = await get_domains_for_project(
            db=db,
            project_id=project_id.project_id,
        )

        logger.info(f'Get {len(project_domains)} domains for project with id {project_id.project_id}')
        domains = _create_list_with_domains(project_domains=project_domains)

        trash_pattern = _generate_regexp_pattern_for_project_domains(domains=domains)
        logger.info(f'Create Regex pattern for project with id {project_id.project_id}')

        result.append(
            RulesData(project_id=project_id.project_id, regexp=trash_pattern)
        )

    return result


async def add_regexp_for_projects(db: Connection, project_regexps: list[RulesData]) -> None:
    for project_id, regexp in project_regexps:
        await add_regexp_for_project(
            db=db,
            regexp=regexp,
            project_id=project_id,
        )
        logger.info(f'Insert regex pattern for project {project_id}')


async def main():
    db_obj = Database()
    db = await db_obj.connection

    logger.info(f'Successfully get connection to {DB_PATH.name}')

    projects_id = await get_unique_projects_id(db=db)
    logger.info(f'Get {len(projects_id)} unique projects')

    project_regexps = await create_regex_for_projects(db=db, projects=projects_id)
    await add_regexp_for_projects(db=db, project_regexps=project_regexps)

    await db.close()
    logger.info(f'Successfully close connection to {DB_PATH.name}')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)
    asyncio.run(main())
