#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'OnInteractionDo'

    @property
    def _author(self) -> str:
        return 'o19'

    @property
    def _base_namespace(self) -> str:
        return 'on_interaction_do'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '0.0.5'


'''
v0.0.5
    Replace local TranslucencyManager with TS4-Library.OpacityManager
    Tested with DD v5.23 2024-11-20, CB v1.67 2024-11-04, HIU v0.3j 2024-09-14
v0.0.4
    Added support for child birth mod CMB pandasama.com/child-birth-mod/
v0.0.3
    Fixed error in mod_data/patch_xml/cfg/nsfw_no_shower_privacy.txt
v0.0.2
    Tested with DD 5.22
v0.0.2
    Releasing a beta
    External config files are still not read.
    Updated support for some devices by Kritical
    Added support for HIU
v0.0.1
    Initial version, refactoring some code
'''
