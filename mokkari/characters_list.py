from marshmallow import ValidationError

from . import character, exceptions


class CharactersList:
    def __init__(self, response):
        self.characters = []
        self.response = response

        schema = character.CharacterSchema()
        for character_dict in response["results"]:
            try:
                result = schema.load(character_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.characters.append(result)

    def __iter__(self):
        return iter(self.characters)

    def __len__(self):
        return len(self.characters)
