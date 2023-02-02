"""
create users table
"""

from yoyo import step

__depends__ = {"create-user-roles-table"}

steps = [
    step(
        """
            create table if not exists users(
                id serial primary key,
                username text unique not null,
                password bytea not null,
                phone_number text unique not null,
                is_active boolean default false not null,
                role_id int references user_roles(id) on delete cascade
            )
        """,
        """
            drop table if exists users; 
        """,
    )
]
