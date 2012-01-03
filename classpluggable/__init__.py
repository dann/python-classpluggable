#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    classpluggable is the .

    It provides .

    :copyright: (c) 2011 by dann.
    :license: BSD, see LICENSE for more details.
"""

import os
import sys


class Plugin(object):

    pass


class PluginLoader(object):

    def __init__(self):
        self.plugins = []

    def load_plugins(self, plugin_dir):
        plugins = self._find_plugins(plugin_dir)
        self._import_plugins(plugin_dir, plugins)
        self._register_plugins()
        return self.plugins

    def _find_plugins(self, plugin_dir):
        plugin_files = [f[:-3] for f in os.listdir(plugin_dir)
                        if f.endswith('.py') and not f.startswith('_')]
        return plugin_files

    def _import_plugins(self, plugin_dir, plugin_files):
        sys.path.insert(0, plugin_dir)
        for plugin in plugin_files:
            try:
                __import__(plugin)
            except ImportError, e:
                print "couldn't load %s: %s" % (plugin, e)

    def _register_plugins(self):
        for plugin in Plugin.__subclasses__():
            self.plugins.append(plugin())


