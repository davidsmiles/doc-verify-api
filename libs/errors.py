from flask_restful import HTTPException
from libs.strings import gettext


class ExpiredTokenLoader(HTTPException):
    pass


class InvalidTokenLoader(HTTPException):
    pass


class MissingTokenLoader(HTTPException):
    pass


class TokenNotFreshCallback(HTTPException):
    pass


class RevokedTokenLoader(HTTPException):
    pass


class UserEmailExists(HTTPException):
    pass


class UserNotExist(HTTPException):
    pass


class EmailInvalid(HTTPException):
    pass


class UserNotConfirmed(HTTPException):
    pass


class UserCartEmpty(HTTPException):
    pass


class ProductNotInCart(HTTPException):
    pass


class QueryInvalidError(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


class ResourceExists(HTTPException):
    pass


class ResourceNotExist(HTTPException):
    pass


class SchemaValidationError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


errors = {
    "ExpiredTokenLoader": {
        'message': 'The token has expired.',
        'status': '401'
    },
    "InvalidTokenLoader": {
        'message': 'Signature verification failed.',
        'status': '401'
    },
    "MissingTokenLoader": {
        "message": "Request does not contain an access token.",
        'status': '401'
    },
    "TokenNotFreshCallback": {
        "message": "The token is not fresh.",
        'status': '401'
    },
    "RevokedTokenLoader": {
        "message": "The token has been revoked.",
        'status': '401'
    },
    "UserEmailExists": {
        "message": gettext("user_email_exists"),
        "status": 409
    },
    "UserNotExist": {
        "message": gettext("user_not_found"),
        "status": 404
    },
    "EmailInvalid": {
        "message": gettext("email_invalid"),
        "status": 400
    },
    "UserNotConfirmed": {
        "message": gettext("user_not_confirmed"),
        "status": 401
    },
    "UserCartEmpty": {
        "message": gettext('user_cart_is_empty'),
        "status": 204
    },
    "ProductNotInCart": {
        "message": gettext('product_not_in_cart'),
        "status": 404
    },
    "UnauthorizedError": {
        "message": gettext("user_invalid_credentials"),
        "status": 401
    },
    "QueryInvalidError": {
        "message": gettext('unexpected_user_data'),
        "status": 500
    },
    "InternalServerError": {
        "message": "Oops, something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "ResourceExists": {
        "message": "This resource already exists",
        "status": 404
    },
    "ResourceNotExist": {
        "message": "The resource you requested could not be found",
        "status": 404
    }
}
