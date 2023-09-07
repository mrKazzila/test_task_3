from aiosqlite import Connection

from project_data_types import Domain, ProjectID


class DomainsServices:

    @classmethod
    async def get_unique_projects_id(cls, db: Connection) -> list[ProjectID]:
        cursor = await db.cursor()
        query = await cursor.execute(
            """
            SELECT DISTINCT project_id
            FROM domains
            """
        )

        rows = await query.fetchall()
        return [ProjectID(project_id[0]) for project_id in rows]

    @classmethod
    async def get_domains_by_project_id(cls, db: Connection, project_id: str) -> list[Domain]:
        cursor = await db.cursor()
        query = await cursor.execute(
            """
            SELECT name
            FROM domains
            WHERE project_id = ?
            """,
            (project_id,),
        )

        rows = await query.fetchall()
        return [Domain(domain[0]) for domain in rows]

    @classmethod
    async def insert_or_replace_regexp_pattern(cls, db: Connection, regexp_pattern: str, project_id: str) -> None:
        cursor = await db.cursor()
        await cursor.execute(
            """
            INSERT OR REPLACE INTO rules (regexp, project_id)
            VALUES (?, ?)
            """,
            (regexp_pattern, project_id),
        )

        await db.commit()
