"""
Issue module.

This module provides the following classes:

- Role
- RolesSchema
- Credit
- CreditsSchema
- Issue
- IssueSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load

from mokkari import arc, character, publisher, series, team, variant


class Role:
    """
    The Role object contains information for creators' role.

    :param `**kwargs`: The keyword arguments is used for setting role data from Metron.
    """

    def __init__(self, **kwargs):
        """Intialize a new Role."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class RolesSchema(Schema):
    """Schema for the Roles."""

    id = fields.Int()
    name = fields.Str()

    @post_load
    def make_object(self, data, **kwargs):
        """
        Make the Role object.

        :param data: Data from Metron response.

        :returns: :class:`Role` object
        :rtype: Role
        """
        return Role(**data)


class Credit:
    """
    The Credit object contains information for creators credits for an issue.

    :param `**kwargs`: The keyword arguments is used for setting creator credit data.
    """

    def __init__(self, **kwargs):
        """Intialize a new Credit."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreditsSchema(Schema):
    """Schema for the Credits."""

    id = fields.Int()
    creator = fields.Str()
    role = fields.Nested(RolesSchema, many=True)

    @post_load
    def make_object(self, data, **kwargs):
        """
        Make the Credit object.

        :param data: Data from Metron response.

        :returns: :class:`Credit` object
        :rtype: Credit
        """
        return Credit(**data)


class Issue:
    """
    The Issue object contains information for an issue.

    :param `**kwargs`: The keyword arguments is used for setting issue data from Metron.
    """

    def __init__(self, **kwargs):
        """Intialize a new Issue."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueSchema(Schema):
    """
    Schema for the Issue API.

    .. versionchanged:: 0.1.6

        - ``name`` field  changed to ``story_titles``
        - ``__str__`` field change to ``issue_name``

    .. versionchanged:: 0.2.0
        Added ``price`` and ``sku`` fields

    .. versionchanged:: 0.2.2
        Added ``upc`` field

    .. versionchanged:: 0.2.4

        - Added ``page_count`` field
        - Changed ``price`` field from a string to float value.

    .. versionchanged:: 1.0.0

        - Changed ``price`` field to a decimal type.

    """

    id = fields.Int()
    publisher = fields.Nested(publisher.PublisherSchema)
    series = fields.Nested(series.SeriesSchema)
    volume = fields.Int()
    number = fields.Str()
    story_titles = fields.List(fields.Str(allow_none=True), data_key="name")
    cover_date = fields.Date()
    store_date = fields.Date(allow_none=True)
    price = fields.Decimal(places=2, allow_none=True)
    sku = fields.Str()
    upc = fields.Str()
    page_count = fields.Int(allow_none=True, data_key="page")
    desc = fields.Str(allow_none=True)
    image = fields.URL()
    arcs = fields.Nested(arc.ArcSchema, many=True)
    credits = fields.Nested(CreditsSchema, many=True)
    characters = fields.Nested(character.CharacterSchema, many=True)
    teams = fields.Nested(team.TeamSchema, many=True)
    issue_name = fields.Str(data_key="__str__")
    variants = fields.Nested(variant.VariantSchema, many=True)
    modified = fields.DateTime()

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE
        datetime = "%Y-%m-%dT%H:%M:%S%z"

    @post_load
    def make_object(self, data, **kwargs):
        """
        Make the arc object.

        :param data: Data from Metron response.

        :returns: :class:`Issue` object
        :rtype: Issue
        """
        return Issue(**data)
