# Resources
from resources.keys import PrivateKey, PublicKey
from resources.login import Login
from resources.signature import Signature
from resources.signup import AdminSignup, Signup
from resources.verification import Verification, StudentImage


def initialize_routes(api):
    api.add_resource(Signup, '/signup')
    api.add_resource(AdminSignup, '/admin/signup')
    api.add_resource(Login, '/login')
    api.add_resource(PrivateKey, '/privatekey')
    api.add_resource(PublicKey, '/publickey')
    api.add_resource(Signature, '/sign')
    api.add_resource(Verification, '/verify')
    api.add_resource(StudentImage, '/student/<doc_id>/image')

