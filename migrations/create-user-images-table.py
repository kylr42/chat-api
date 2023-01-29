"""
create user images table
"""

from yoyo import step

__depends__ = {"create-refresh-tokens-table"}

steps = [
    step(
        """
            create table if not exists user_images(
                id serial primary key,
                url text unique not null,
                created_at timestamp default now() not null,
                updated_at timestamp default now() not null,
                user_id int references users(id) on delete cascade
            );
        """,
        """
            drop table if exists user_images; 
        """,
    )
]
