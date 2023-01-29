"""
create users table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists users(
                id serial primary key,
                username text unique not null,
                password bytea not null,
                password_updated_at timestamp default now() not null,
                phone_number text unique not null,
                is_active boolean default false not null
            )
        """,
        """
            drop table if exists users; 
        """,
    )
]
