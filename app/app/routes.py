from flask import Blueprint
from .apis import upload_file

rest_api = Blueprint('rest api', __name__)

rest_api.route('/upload/', methods=('POST',))(upload_file)
