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
                room_id int references rooms(id) on delete cascade,
                is_archived boolean default false not null,
                is_favorite boolean default false not null,
                constraint values_in_row_must_be_unique unique (
                    user_id, room_id
                )
            );
        """,
        """
            drop table if exists user_room_mapping; 
        """,
    )
]
