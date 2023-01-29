"""
create user to room mapping table
"""

from yoyo import step

__depends__ = {"create-room-table", "create-users-table"}

steps = [
    step(
        """
            create table if not exists user_room_mapping(
                id serial primary key,
                user_id int references users(id) on delete cascade,
                room_id varchar references rooms(id) on delete cascade,
                is_archived boolean default false not null,
                is_favorite boolean default false not null
            );
        """,
        """
            drop table if exists user_room_mapping; 
        """,
    )
]
