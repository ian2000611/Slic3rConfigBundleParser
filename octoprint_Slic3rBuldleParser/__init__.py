# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import configparser
import octoprint.plugin

class Slic3rbuldleparserPlugin(octoprint.plugin.SettingsPlugin,
                               octoprint.plugin.AssetPlugin,
                               octoprint.plugin.TemplatePlugin,
							   octoprint.plugin.StartupPlugin):
	def on_after_startup(self):
		manager = self._slicing_manager
		slicers = manager.registered_slicers
		for s in slicers:
			self._logger.info("slicer:" + s)

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/Slic3rBuldleParser.js"],
			css=["css/Slic3rBuldleParser.css"],
			less=["less/Slic3rBuldleParser.less"]
		)

	##-- Main functions 

	def do_config(data):
		data = parse_config(data)
		if (data):
			make_configs(adata,data["presets"]["printer"])
			return true
		return false

	def parse_config(data):
		manager = self._slicing_manager
		slicers = manager.registered_slicers
		for s in slicers:
			self._logger.info("slicer:" + s)
		config = configparser.ConfigParser()
		if (data.readline().contains("Slic3r")):
			config.readfp(data,'upload')
			parts = {}
			parts['presets'] = {}	
			for s in config.sections():
				store = parts['presets']
				if s.contains(":"):
					names = s.split(":",1)
					parts[names[0]] = parts.get(names[0],{})
					parts[names[0]][names[1]] = parts[names[0]].get(names[1],{})
					store = parts[names[0]][names[1]]
				for o in config.options(s):
					store[o] = config.get(s,o)
			return parts
		return false

	def make_configs(data,printer):
		for q in data["print"]:
			for f in data["filament"]:
				file = data["printer"][printer].copy()
				file.update(data["print"][q])
				file.update( data["filament"][f])




	def fileupload(path, file_object, links=None, printer_profile=None, allow_overwrite=False, *args, **kwargs):
		if do_config(file_object.stream()):
			return None
		return file_object

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			Slic3rBuldleParser=dict(
				displayName="Slic3rbuldleparser Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="ian2000611",
				repo="Slic3rConfigBundleParser",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/ian2000611/Slic3rConfigBundleParser/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Slic3rbuldleparser Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Slic3rbuldleparserPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.filemanager.preprocessor": __plugin_implementation__.
	}

