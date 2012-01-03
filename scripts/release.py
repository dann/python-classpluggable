#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    release
    ~~~~~~~

    Helper script that performs a release.

    :copyright: (c) 2011 by Dann
    :license: BSD, see LICENSE.txt for more details.
"""
import sys
import os
import re
from subprocess import Popen, PIPE


def get_release_version():
    with open('CHANGES.rst') as f:
        lineiter = iter(f)
        for line in lineiter:
            match = re.search('^Version\s+(.*)', line.strip())
            if match is None:
                continue
            version = match.group(1).strip()
            return version


def check_release(version):
    log_info("Checking release: %s", version)
    check_is_repo_clean()
    check_version_isnt_in_tags(version)


def check_version_isnt_in_tags(version):
    tags = get_git_tags()

    if version in tags:
        log_fail('Version "%s" is already tagged', version)


def check_is_repo_clean():
    if not is_git_clean():
        log_fail('You have uncommitted changes in git')


def get_git_tags():
    return set(Popen(['git', 'tag'], stdout=PIPE).communicate()[0].splitlines())


def is_git_clean():
    return Popen(['git', 'diff', '--quiet']).wait() == 0


def make_git_commit(message, *args):
    message = message % args
    Popen(['git', 'commit', '-am', message]).wait()


def make_git_tag(tag):
    log_info('Tagging "%s"', tag)
    Popen(['git', 'tag', tag]).wait()


def build_and_upload():
    log_info('Building and uploading to PyPI ...');
    Popen([sys.executable, 'setup.py', 'release', 'sdist', 'upload']).wait()


def log_fail(message, *args):
    print >> sys.stderr, 'Error:', message % args
    sys.exit(1)


def log_info(message, *args):
    print >> sys.stderr, message % args


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

    version = get_release_version()
    if version is None:
        log_fail('Could not get the version from changelog.')

    log_info('Releasing %s', version)

    check_release(version)
    make_git_commit('Bump version number to %s', version)
    make_git_tag(version)
    build_and_upload()


if __name__ == '__main__':
    main()