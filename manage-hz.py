#!/usr/bin/env python2

from flask.ext.script import Manager
from hackzurich import create_app
from hackzurich import crawler


manager = Manager(create_app)


@manager.option('-v', '--verbose', help='Print a log')
def crawl():
    crawler.crawl()


@manager.command
def wsgi():
    pass


if __name__ == '__main__':
    manager.run()
