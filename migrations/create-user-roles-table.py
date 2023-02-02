"""
create user_roles table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists user_roles(
                id serial primary key,
                role_name varchar(20) unique not null
            );
        """,
        """
            drop table if exists user_roles;
        """,
    )
]
