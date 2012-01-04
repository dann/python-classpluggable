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
        self.suffix = '.py'

    def load_plugins(self, plugin_dirs):
        if len(self.plugins) > 0:
            return self.plugins

        for plugin_dir in plugin_dirs:
            self.load_plugins_in(plugin_dir)

        return self.plugins

    def load_plugins_in(self, plugin_dir):
        plugins = self._find_plugins(plugin_dir)
        self._add_path_to_plugins(plugin_dir)
        self._import_plugins(plugins)
        self._register_plugins()
        return self.plugins

    def _find_plugins(self, plugin_dir):
        plugin_files = [f[:-3] for f in os.listdir(plugin_dir)
                        if f.endswith(self.suffix)
                        and not f.startswith('_')]
        return plugin_files

    def _add_path_to_plugins(self, plugin_dir):
        sys.path.insert(0, plugin_dir)

    def _import_plugins(self, plugin_files):
        for plugin in plugin_files:
            self._import_module(plugin)

    def _import_module(self, module):
        try:
            __import__(module)
        except ImportError, e:
            print "Couldn't load %s: %s" % (module, e)

    def _register_plugins(self):
        for plugin in Plugin.__subclasses__():
            self.plugins.append(plugin())

    def reload_plugins(self, plugin_dir):
        self.plugins = []
        return self.load_plugins(plugin_dir)


