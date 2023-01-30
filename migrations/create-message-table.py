"""
create user to room mapping table
"""

from yoyo import step

__depends__ = {"create-room-table", "create-users-table", "create-message-type-table"}

steps = [
    step(
        """
            create table if not exists messages(
                id serial primary key,
                message text not null,

                created_at timestamp default now() not null,
                updated_at timestamp default now() not null,

                room_id int references rooms(id) on delete cascade,
                user_id int references users(id) on delete cascade,
                message_type_id int references message_types(id) on delete cascade
            )
        """,
        """
            drop table if exists messages 
        """,
    )
]
