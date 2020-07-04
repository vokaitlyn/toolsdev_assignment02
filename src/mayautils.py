# Kaitlyn Vo
# ATCM 3311.0U1 - Assignment 02
# 07/04/2020

import logging

import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


class SceneFile(object):
    """Initialises attributes when class is instantiated"""
    def __init__(self, dir='', descriptor='main', version=1, ext="ma"):
        if pmc.system.isModified():
            self.dir = Path(dir)
            self.descriptor = descriptor
            self.version = version
            self.ext = ext
        else:
            temp_path = Path(pmc.system.sceneName())
            self.dir = temp_path.parent

            file_name = temp_path.name
            file_part = file_name.split("_v")
            if len(file_part) != 2:
                raise RuntimeError("File name must contain _v")
            self.descriptor = file_part[0]

            version = file_part[1].split(".")[0]
            self.version = int(version)

            self.ext = file_part[1].split(".")[1]

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, val):
        self._dir = Path(val)

    """Return a scene file name"""
    def basename(self):
        name_pattern = "{descriptor}_v{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor,
                                   version=self.version,
                                   ext=self.ext)
        return name

    """Retuns a path to scene file"""
    def path(self):
        return Path(self.dir) / self.basename()

    """Saves the scene file"""
    def save(self):
        try:
            pmc.system.saveAs(self.path())
        except RuntimeError:
            log.warning("Missing directories. Creating directories.")
            self.dir.makedirs_p()
            pmc.system.saveAs(self.path())

    """Increments the version and saves the scene file, incrementing from next largest number available."""
    def increment_and_save(self):
        files_list = self.dir.listdir()
        scene_list = list()
        for file in files_list:
            file_path = Path(file)
            scene = file_path.name
            if self.is_scene_file(scene):
                scene_list.append(scene)
        new_version = self.version

        current_scenes = [x for x in scene_list if x.split("_v")[0] == self.descriptor]
        for scene in current_scenes:
            version_name = scene.split("_v")[1].split(".")[0]
            version = int(version_name)
            if version > self.version:
                new_version = version

        self.version = new_version + 1
        self.save()

    def is_scene_file(self, filename):
        file_parts = filename.split("_v")
        if len(file_parts) != 2:
            return False
        file_version = file_parts[1].split(".")
        if len(file_version) != 2:
            return False
        if file_version[1] != "ma":
            return False
        if len(file_version[0]) != 3 or not file_version[0].isdigit():
            return False
        return True
