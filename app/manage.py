# manage.py


import unittest

import coverage
from flask import cli

from app import create_app

COV = coverage.coverage(
    config_file=True,
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*',
        'app/config.py',
        'app/__init__.py'
    ]
)
COV.start()

app = create_app()


@app.cli.command()
@cli.with_appcontext
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command()
@cli.with_appcontext
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('app/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report(directory='htmlcov')
        COV.erase()
        return 0
    return 1


@app.cli.command()
@cli.with_appcontext
def shell_plus():
    import os
    from IPython import embed
    embed(user_ns={'app': app, os: 'os'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
