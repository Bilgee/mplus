#!/usr/bin/python
# coding: utf-8
""" Filename:     runserver.py
    Purpose:      This file runs the Flask application service
    Requirements: Flask
"""
from application import app as application
from config import HTTP_PORT, HTTP_HOST

if __name__ == '__main__':
    application.run(host=HTTP_HOST, port=HTTP_PORT, debug=False)
