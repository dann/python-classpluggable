#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from nose.tools import ok_
from classpluggable import PluginLoader


def test_load_plugins():
    plugin_dir = \
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     'plugins')
    loader = PluginLoader()
    plugins = loader.load_plugins([plugin_dir])
    ok_(len(plugins) == 2)

    for plugin in plugins:
        result = plugin.calc()
        ok_(result == 1)


