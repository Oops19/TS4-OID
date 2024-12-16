#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import ast
import os
from typing import Dict

from on_interaction_do.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.libraries.file_utils import FileUtils
from ts4lib.libraries.ts4folders import TS4Folders

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class UserConfig:  # TODO change to (metaclass=Singleton):
    def __init__(self):
        self.ts4f = TS4Folders(ModInfo.get_identity().base_namespace)
        self.config_folder = os.path.join(self.ts4f.data_folder, 'cfg')
        self.fu = FileUtils(os.path.join(self.config_folder))
        self._configuration_data: Dict = {}
        self.merge_configuration_files()

    def merge_configuration_files(self) -> bool:
        parse_error = False
        configuration_data: Dict = {}
        files = self.fu.find_files(r'^.*debug\.txt$')
        if not files:
            files = self.fu.find_files(r'^.*\.txt$')
        log.enable()
        log.debug(f"Reading '{files}'")
        for file in files:
            try:
                with open(file, mode='rt', encoding='UTF-8') as fp:
                    data = ast.literal_eval(fp.read())
                    configuration_data.update(data)
            except Exception as e:
                log.warn(f"Skipping file '{file}' with error '{e}'.")
                parse_error = True
        log.debug(f"Merged configuration files: -> {configuration_data}")
        self._configuration_data = configuration_data
        return parse_error

    def update_configuration_files(self) -> bool:
        return self.merge_configuration_files()

    @property
    def configuration_data(self) -> Dict:
        return self._configuration_data.copy()
