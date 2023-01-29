"""
create user to room mapping table
"""

from yoyo import step

__depends__ = {"create-refresh-tokens-table"}

steps = [
    step(
        """
            create table if not exists user_room_mapping(
                id serial primary key,
                foreign key (user_id) references users(id) on delete cascade,
                foreign key (room_id) references rooms(id) on delete cascade,
                is_archived boolean default false not null,
                is_favorite boolean default false not null,
        """,
        """
            drop table if exists user_room_mapping; 
        """,
    )
]
