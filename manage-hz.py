#!/usr/bin/env python2

from flask.ext.script import Manager
from hackzurich import create_app


manager = Manager(create_app)


if __name__ == '__main__':
    manager.run()
