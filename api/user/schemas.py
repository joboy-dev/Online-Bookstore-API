from marshmallow import Schema, fields, validate

from api.user.models import Role

class UserSchema(Schema):
    '''User schema'''
        
    id = fields.UUID(dump_only=True)
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(required=True)
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=128))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=128))
    profile_pic = fields.String(required=False)
    role = fields.Enum(enum=Role, required=True)
    is_verified = fields.Boolean(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

user_schema = UserSchema(only=['id', 'email', 'first_name', 'last_name', 'role', 'profile_pic', 'last_login'])

register_schema = UserSchema(only=['email', 'password', 'first_name', 'last_name', 'role'])
login_schema = UserSchema(only=['email', 'password'])
update_details_schema = UserSchema(only=['first_name', 'last_name'])
update_email_schema = UserSchema(only=['email'])
