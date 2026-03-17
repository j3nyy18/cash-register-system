from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1)
    )
    phone = fields.String(
        required=True,
        validate=validate.Regexp(r"^\d{10}$", error="Phone must be 10 digits")
    )


class WalletTopupSchema(Schema):
    phone = fields.String(
        required=True,
        validate=validate.Regexp(r"^\d{10}$")
    )
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=1)
    )


class TransactionSchema(Schema):
    phone = fields.String(
        required=True,
        validate=validate.Regexp(r"^\d{10}$")
    )
    bill_amount = fields.Float(
        required=True,
        validate=validate.Range(min=1)
    )
    promo_code = fields.String(required=False)