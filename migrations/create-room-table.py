"""
create room table
"""

from yoyo import step

__depends__ = {"create-refresh-tokens-table", }

steps = [
    step(
        """
            create table if not exists rooms(
                id varchar primary key,
                name text not null,
                description text
            )
        """,
        """
            drop table if exists rooms 
        """,
    )
]
