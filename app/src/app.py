# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import sys
import logging
from logstash_async.handler import AsynchronousLogstashHandler
from flask import Flask, request, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from http import HTTPStatus
from . import config
from .modules import mod_registration as reguser
from .modules import mod_authentication as authuser
from .modules import mod_restore as restore

logger = logging.getLogger('python-logstash-logger')
logger.setLevel(logging.INFO)
logger.addHandler(AsynchronousLogstashHandler(
    config.LOGSTASH_HOST,
    config.LOGSTASH_PORT,
    config.LOGSTASH_INTERNAL_DB
))

try:
    application = Flask(config.APPLICATION)
    limiter = Limiter(
        application,
        key_func=get_remote_address,
        default_limits=[config.APPLICATION_LIMIT_PER_MIN, config.APPLICATION_LIMIT_PER_SEC],
        headers_enabled=True,
        storage_uri=config.APPLICATION_LIMIT_STORAGE_URI
    )

    """
    @api {post} /registration/s1 Register new user (Step 1)
    @apiName Registration (Step 1)
    @apiGroup Access API
    @apiDescription Providing first-step registration process
    @apiPermission user
    @apiParam {String} phone User phone
    @apiSuccess {Number} status HTTP 201 Created
    @apiSuccess {Object[]} message  Provision of a code to confirm registration

    @apiSuccessExample Success-Response
        HTTP/1.1 201 Created
        {
            "message": {
                "code" : "xxxxx"
            }
        }

    @apiError RegistrationRequestError Invalid request data
    @apiErrorExample RegistrationRequestError
        HTTP/1.1 400 Bad Request
        {
            "message": [
                "Please provide a valid phone number.", 
                "Length must be between 5 and 12"
            ],
        }

    @apiError RegistrationConflictError The user already registered
    @apiErrorExample RegistrationConflictError
        HTTP/1.1 409 Conflict
        {
            "message": "The user already registered"
        }   
        
    @apiError TooManyRequestsError Too many requests to node
    @apiErrorExample TooManyRequestsError
        HTTP/1.1 429 Too many requests
        {
            "message": "The user has sent too many requests in a given amount of time ("rate limiting")"
        }  
        
    @apiError RegistrationUnavailableError The server cannot process the request
    @apiErrorExample RegistrationUnavailableError
        HTTP/1.1 503 Service Temporary Unavailable
        {
            "message": "The server cannot process the request due to a high load"
        }        
    """


    @application.route('/registration/s1', methods=['POST'])
    @limiter.limit(config.APPLICATION_LIMIT_REG)
    def registration_s1():
        """
        User mod_registration release
        Providing first-step registration process
        :return: str
        """

        try:
            message = reguser.step_one(request.form)
            return make_response(jsonify(
                message=message
            ), HTTPStatus.CREATED)
        except reguser.RegistrationRequestError as e:
            logging.exception(e)
            return bad_request(e.message)
        except reguser.RegistrationConflictError as e:
            logging.exception(e)
            return conflict(e.message)
        except (reguser.RegistrationUnavailableError, Exception) as e:
            logging.critical(e)
            return service_unavailable()


    """
    @api {post} /registration/s2 Confirm user registration (Step 2)
    @apiName Registration (Step 2)
    @apiGroup Access API
    @apiDescription Providing second-step registration process
    @apiPermission user
    @apiParam {String} phone User phone
    @apiParam {Number} code User verification code
    @apiSuccess {Number} status HTTP 201 Created
    @apiSuccess {Object[]} message  Issuance of data for authentication

    @apiSuccessExample Success-Response
        HTTP/1.1 201 Created
        {
            "message": {
                "password": "xxxxxxxx",
                "phone": xxxxxxxxxxx,
                "user_id": 1
            }
        }

    @apiError RegistrationRequestError Invalid request data
    @apiErrorExample RegistrationRequestError
        HTTP/1.1 400 Bad Request
        {
            "message": [
                "Please provide a valid phone number.", 
                "Length must be between 5 and 12"
                "Please provide a valid code.", 
                "Length must be equal 5 chars"
            ],
        }  
        
    @apiError TooManyRequestsError Too many requests to node
    @apiErrorExample TooManyRequestsError
        HTTP/1.1 429 Too many requests
        {
            "message": "The user has sent too many requests in a given amount of time ("rate limiting")"
        }  
        
    @apiError RegistrationUnavailableError The user already exist
    @apiErrorExample RegistrationUnavailableError
        HTTP/1.1 503 Service Temporary Unavailable
        {
            "message": "The server cannot process the request due to a high load"
        }    
    """


    @application.route('/registration/s2', methods=['POST'])
    @limiter.limit(config.APPLICATION_LIMIT_REG)
    def registration_s2():
        """
        User mod_registration release
        Providing second-step registration process
        :return: str
        """

        try:
            message = reguser.step_two(request.form)
            return make_response(jsonify(
                message=message
            ), HTTPStatus.CREATED)
        except reguser.RegistrationRequestError as e:
            logging.exception(e)
            return bad_request(e.message)
        except (reguser.RegistrationUnavailableError, Exception) as e:
            logging.critical(e)
            return service_unavailable()


    """
    @api {post} /authentication Authenticate user
    @apiName Authentication
    @apiGroup Access API
    @apiDescription Providing user authentication process
    @apiPermission user
    @apiParam {String} phone User phone
    @apiParam {String} password User password
    @apiSuccess {Number} status HTTP 200 OK
    @apiSuccess {Object[]} message  Get auth token

    @apiSuccessExample Success-Response
        HTTP/1.1 200 OK
        {
            "message": {
                "expires": 1509010463,
                "token": "XXX.XXX.XXX"
            }
        }

    @apiError AuthenticationRequestError Invalid request data
    @apiErrorExample AuthenticationRequestError
        HTTP/1.1 400 Bad Request
        {
            "message": [
                "Please provide a valid phone number.", 
                "Length must be between 5 and 12"
                "Please provide a valid code.", 
                "Length must be equal 5 chars"
            ],
        }

    @apiError AuthenticationForbiddenError Invalid credentials
    @apiErrorExample AuthenticationForbiddenError
        HTTP/1.1 403 Forbidden
        {
            "message": "Invalid credentials"
        }  
        
    @apiError AuthenticationNotFoundError User not found
    @apiErrorExample AuthenticationNotFoundError
        HTTP/1.1 404 Not Found
        {
            "message": "User not found"
        }     
          
    @apiError TooManyRequestsError Too many requests to node
    @apiErrorExample TooManyRequestsError
        HTTP/1.1 429 Too many requests
        {
            "message": "The user has sent too many requests in a given amount of time ("rate limiting")"
        }    
    """


    @application.route('/authentication', methods=['POST'])
    @limiter.limit(config.APPLICATION_LIMIT_AUTH)
    def authentication():
        """
        User mod_authentication release
        Providing user authentication process
        :return: str
        """

        try:
            message = authuser.login(request.form)
            return make_response(jsonify(
                message=message
            ), HTTPStatus.OK)
        except authuser.AuthenticationRequestError as e:
            logging.exception(e)
            return bad_request(e.message)
        except authuser.AuthenticationNotFoundError as e:
            logging.error(e)
            return not_found(e.message)
        except authuser.AuthenticationForbiddenError as e:
            logging.error(e)
            return forbidden(e.message)
        except Exception as e:
            logging.critical(e)
            print(e)
            return service_unavailable()


    """
    @api {post} /restore/s1 Restore user access (Step 1)
    @apiName Restore (Step 1)
    @apiGroup Access API
    @apiDescription  Providing first-step of access recovering
    @apiPermission user
    @apiParam {String} phone User phone
    @apiSuccess {Number} status HTTP 201 Created
    @apiSuccess {Object[]} message  Provision of a code to confirm restore process

    @apiSuccessExample Success-Response
        HTTP/1.1 201 Created
        {
            "message": {
                "code" : "xxxxx"
            }
        }

    @apiError RestoreRequestError Invalid request data
    @apiErrorExample RestoreRequestError
        HTTP/1.1 400 Bad Request
        {
            "message": [
                "Please provide a valid phone number.", 
                "Length must be between 5 and 12"
            ],
        }

    @apiError RestoreNotFoundError User not found
    @apiErrorExample RestoreNotFoundError
        HTTP/1.1 404 Not Found
        {
            "message": "User not found"
        }   

    @apiError TooManyRequestsError Too many requests to node
    @apiErrorExample TooManyRequestsError
        HTTP/1.1 429 Too many requests
        {
            "message": "The user has sent too many requests in a given amount of time ("rate limiting")"
        }  

    @apiError RegistrationUnavailableError The server cannot process the request
    @apiErrorExample RegistrationUnavailableError
        HTTP/1.1 503 Service Temporary Unavailable
        {
            "message": "The server cannot process the request due to a high load"
        }        
    """


    @application.route('/restore/s1', methods=['POST'])
    @limiter.limit(config.APPLICATION_LIMIT_RESTORE)
    def restore_s1():
        """
        User mod_restore release
         Providing second-step of recovering
        :return: str
        """

        try:
            message = restore.step_one(request.form)
            return make_response(jsonify(
                message=message
            ), HTTPStatus.CREATED)
        except restore.RestoreRequestError as e:
            logging.exception(e)
            return bad_request(e.message)
        except restore.RestoreNotFoundError as e:
            logging.exception(e)
            return not_found(e.message)
        except (restore.RestoreUnavailableError, Exception) as e:
            logging.critical(e)
            print(e)
            return service_unavailable()


    """
    @api {post} /restore/s2 Confirm user restore process (Step 2)
    @apiName Restore (Step 2)
    @apiGroup Access API
    @apiDescription Providing second-step of access recovering
    @apiPermission user
    @apiParam {String} phone User phone
    @apiParam {Number} code User verification code
    @apiSuccess {Number} status HTTP 201 Created
    @apiSuccess {Object[]} message  Issuance of data for authentication

    @apiSuccessExample Success-Response
        HTTP/1.1 201 Created
        {
            "message": {
                "password": "xxxxxxxx",
                "phone": xxxxxxxxxxx,
                "user_id": 1
            }
        }

    @apiError RestoreRequestError Invalid request data
    @apiErrorExample RestoreRequestError
        HTTP/1.1 400 Bad Request
        {
            "message": [
                "Please provide a valid phone number.", 
                "Length must be between 5 and 12"
                "Please provide a valid code.", 
                "Length must be equal 5 chars"
            ],
        }  

    @apiError TooManyRequestsError Too many requests to node
    @apiErrorExample TooManyRequestsError
        HTTP/1.1 429 Too many requests
        {
            "message": "The user has sent too many requests in a given amount of time ("rate limiting")"
        }  

    @apiError RegistrationUnavailableError The user already exist
    @apiErrorExample RegistrationUnavailableError
        HTTP/1.1 503 Service Temporary Unavailable
        {
            "message": "The server cannot process the request due to a high load"
        }    
    """


    @application.route('/restore/s2', methods=['POST'])
    @limiter.limit(config.APPLICATION_LIMIT_RESTORE)
    def restore_s2():
        """
        User mod_restore release
        Providing second-step of access recovering
        :return: str
        """

        try:
            message = restore.step_two(request.form)
            return make_response(jsonify(
                message=message
            ), HTTPStatus.CREATED)
        except restore.RestoreRequestError as e:
            logging.exception(e)
            return bad_request(e.message)
        except (restore.RestoreUnavailableError, Exception) as e:
            logging.critical(e)
            print(e)
            return service_unavailable()


    @application.errorhandler(HTTPStatus.SERVICE_UNAVAILABLE)
    def service_unavailable():
        """
        HTTP 503 / Service Temporary Unavailable
        :return: str
        """

        return make_response(jsonify(
            message=HTTPStatus.SERVICE_UNAVAILABLE.description
        ), HTTPStatus.SERVICE_UNAVAILABLE)


    @application.errorhandler(HTTPStatus.FORBIDDEN)
    def forbidden(errmsg):
        """
        HTTP 403 / Forbidden
        :param errmsg: str
        :return: str
        """

        return make_response(jsonify(
            message=errmsg
        ), HTTPStatus.FORBIDDEN)


    @application.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(errmsg):
        """
        HTTP 400 / Bad request
        :param errmsg: str
        :return: str
        """

        return make_response(jsonify(
            message=errmsg
        ), HTTPStatus.BAD_REQUEST)


    @application.errorhandler(HTTPStatus.CONFLICT)
    def conflict(errmsg):
        """
        HTTP 409 / Conflict
        :param errmsg: str
        :return: str
        """

        return make_response(jsonify(
            message=errmsg
        ), HTTPStatus.CONFLICT)


    @application.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(errmsg):
        """
        HTTP/1.1 404 Page not found
        :param errmsg: str
        :return: str
        """

        return make_response(jsonify(
            message=str(errmsg)
        ), HTTPStatus.NOT_FOUND)


    @application.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
    def too_many_requests(errmsg):
        """
        HTTP/1.1 429 Too many requests
        :param errmsg: str
        :return: str
        """

        return make_response(jsonify(
            message=str(errmsg)
        ), HTTPStatus.TOO_MANY_REQUESTS)

except Exception as error:
    logging.critical(error)
    sys.exit(error)
