#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from on_interaction_do.modinfo import ModInfo
from ts4lib.utils.singleton import Singleton
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class DcCache(metaclass=Singleton):
    def __init__(self):
        self._failure = True
        try:
            from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
            from deviantcore.utils.sexual_organ_utils import DCSexualOrganUtils

            from deviousdesires.nudity_system.enums.part_handle_type import DDPartHandleType
            from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
            from deviousdesires.nudity_system.utils.penis_state_utils import DDPenisStateUtils
            from deviousdesires.sex.enums.string_ids import DDSexSystemStringId
            self._failure = False
        except Exception as e:
            log.warn(f"Could not import all required libraries! ({e})")
            log.warn(f"'DC/DD will do nothing!")

    @property
    def failure(self) -> bool:
        """
        Use it like this:
        `def foo(...):
            if DcCache().failure:
                return
            pass  # actual code to make use of DC/DD`
        @return: True if DC/DD is not available.
        """
        return self._failure

    @property
    def is_available(self) -> bool:
        return not self._failure
