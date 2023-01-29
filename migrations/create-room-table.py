"""
create room table
"""

from yoyo import step

__depends__ = {"create-user-room-mapping-table"}

steps = [
    step(
        """
            create table if not exists rooms(
                id str primary key,
                name text not null,
                description text
            )
        """,
        """
            drop table if exists rooms 
        """,
    )
]
