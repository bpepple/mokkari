from marshmallow import INCLUDE, Schema, fields, post_load

from mokkari import creator


class Team:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TeamSchema(Schema):
    """ Schema for the Team API."""
    id = fields.Int()
    name = fields.Str()
    desc = fields.Str()
    wikipedia = fields.Str()
    image = fields.Url()
    creators = fields.Nested(creator.CreatorSchema, many=True)

    class Meta:
        unknown = INCLUDE

    @post_load
    def make(self, data, **kwargs):
        return Team(**data)
