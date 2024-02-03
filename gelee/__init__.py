"""Validate configuration files against their format and maybe schema."""

# [[[fill git_describe()]]]
__version__ = '2022.11.28+parent.7cef30b3-dirty'
# [[[end]]] (checksum: 292b24b2ea3ee44d0bfa30684335287e)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
