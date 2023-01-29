"""
create message types table
"""

from yoyo import step

__depends__ = {"create-room-table", }

steps = [
    step(
        """
            create table if not exists message_types(
                id serial primary key,
                name text not null
            )
        """,
        """
            drop table if exists message_types; 
        """,
    )
]
