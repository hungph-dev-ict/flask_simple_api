from app import app
import os
from flask import Flask, request, jsonify, make_response, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random
from PIL import Image

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def random_string(length):
    return ''.join(str(random.randint(0, 9)) for m in xrange(length))


# Error handle
@app.errorhandler(400)
def authentication_fail(error):
    return make_response(jsonify({'error': 'Authentication fail. User key not exist !'}), 400)


@app.errorhandler(401)
def file_format(error):
    return make_response(jsonify({'error': 'Upload file fail. File format is unsupported !'}), 401)


@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Server error !'}), 403)


@app.errorhandler(429)
def limit_error(error):
    return make_response(jsonify({'error': 'Limit 60 requests per minute request error !'}), 429)


@app.errorhandler(411)
def max_size(error):
    return make_response(jsonify({'error': 'Invalid size image uploaded !'}), 411)


# Route define
@app.route('/anpr/v1/', methods=['POST'])
@limiter.limit("60 per minute")
def plateRecognition():
    # Check user_key
    sampleUserKey = 'xxxyyy'
    reqUserKey = request.headers.get('user_key')
    if not reqUserKey == sampleUserKey:
        abort(409)

    # Check file format
    imagePath = request.form.get('image')
    allowExtension = ('.png', '.jpg', '.jpeg')
    if not imagePath.lower().endswith(allowExtension):
        abort(401)

    # Check image size
    try:
        im = Image.open(imagePath)
    except:
        abort(404)
    width, height = im.size
    if width > 544 or height > 544:
        abort(411)

    response = '''
    {
        "number": ''' + str(random_string(9)) + ''',
        "confidence": ''' + str(random.uniform(80.00, 100.00)) + '''  
    } '''

    return jsonify(response), 201
