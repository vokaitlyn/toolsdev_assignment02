import logging

import pymel.core as pmc
from pymel.core.system import Path
from pymel.core.system import versions


log = logging.getLogger(__name__)


class SceneFile(object):

    """Initialises attributes when class is instantiated"""
    def __init__(self, dir='', descriptor='main', version=1, ext="ma"):
        #Delineates between new scene vs open scene with naming conventions
        if pmc.system.isModified():
            self._dir = Path(dir)
            self.descriptor = descriptor
            self.version = version
            self.ext = ext
        else:
            temp_path = Path(pmc.system.sceneName())
            self.dir = temp_path.parent
            file_name = temp_path.name
            try:
                self.descriptor = file_name.split("_v")[0]
                file_version = file_name.split("_v")[1]
                file_version2 = file_name.splt(".")[0]
                self.version = int(file_version2)
                self.ext = file_name.split(".")[1]
            except IndexError:
                self.descriptor = file_name.split("_")[0]
                file_version = file_name.split("_")[1]
                file_version2 = file_version.split(".")[0]
                self.version = int(file_version2)
                self.ext = file_version.split(".")[1]

    
    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self,val):
        self._dir = Path(val)


    """Return a scene file name"""
    def basename(self):
        name_pattern = "{descriptor}_{version:03d}.{ext}"
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
        file_list = pmc.getFileList(folder=self.dir)
        scene_list = list()

        for file in files_list:
            file_path = Path(file)
            scene = file_path.name
            scene_list.append(scene)

        new_version = self.version

        for scene in scene_list:
            descriptor = scene.split("_v")[0]

            if descriptor == self.descriptor:
                version_name = scene.split("_v")[1].split(".")[0]
                version_name2 = version_name.split(".")[0]
                version = int(version_str)

                if version > self.version:
                    new_version = version

        self.version = new_version + 1
        self.save()
