from marshmallow import Schema
from marshmallow.fields import Nested, Str, Dict, Float, Int
from marshmallow.validate import Range


class ConvertSchema(Schema):
    amount = Float(strict=True, required=True)


class ConvertRequestSchema(ConvertSchema):
    to = Str(required=True)

    # from - служебное имя
    class Meta:
        include = {
            'from': Str(required=True)
        }


class ConvertResponseSchema(Schema):
    data = Nested(ConvertSchema(), required=True)


class DatabaseRequestSchema(Schema):
    currencies = Dict(key=Str(), values=Float())


class DatabaseRequestQuerySchema(Schema):
    merge = Int(validate=Range(min=0, max=1), required=True)
