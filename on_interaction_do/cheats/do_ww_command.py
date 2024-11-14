#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from on_interaction_do.cheats.run_after import RunAfter
from on_interaction_do.modinfo import ModInfo
from sims.sim_info import SimInfo
from ts4lib.utils.singleton import Singleton

try:
    from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
    from deviantcore.utils.sexual_organ_utils import DCSexualOrganUtils

    from deviousdesires.nudity_system.enums.part_handle_type import DDPartHandleType
    from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
    from deviousdesires.nudity_system.utils.penis_state_utils import DDPenisStateUtils
    from deviousdesires.sex.enums.string_ids import DDSexSystemStringId
except:
    pass

from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.utils.tuning_helper import TuningHelper

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class DoWwCommand(metaclass=Singleton):
    def __init__(self):
        log.debug(f"Initializing DoWwCommand() ...")
        self.supported_interactions = []
        self.unsupported_interactions = []

        manager = "INTERACTION"
        tunings = ['HIU:*', 'PR:*', ]
        self.supported_interactions = TuningHelper().get_tuning_ids(manager, tunings)

        manager = "INTERACTION"
        tunings = ['Kritical:*', ]
        self.unsupported_interactions = TuningHelper().get_tuning_ids(manager, tunings)

        self.run_after = RunAfter()

    def undress_bottom(self, sim_info: SimInfo, cmd: str, _sim_id: str):
        try:
            log.debug(f"Called(2): {cmd} '{sim_info}'")
            DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE)
        except Exception as e:
            log.error("Error", exception=e, throw=True)

    def equip_strapon(self, sim_info: SimInfo, cmd: str, _sim_id: str):
        try:
            log.debug(f"Called(2): {cmd} '{sim_info}'")
            if DCSexualOrganUtils().has_penis(sim_info):
                DDPenisStateUtils().set_erect(sim_info, DDSexSystemStringId.HAVE_SEX, update_outfit=True)
            elif not DDNuditySystemUtils().has_strapon_equipped(sim_info):
                DDNuditySystemUtils().equip_strapon(sim_info)
        except Exception as e:
            log.error("Error", exception=e, throw=True)

    def remove_strapon(self, sim_info: SimInfo, cmd: str, _sim_id: str):
        try:
            log.debug(f"Called(2): {cmd} '{sim_info}'")
            if DCSexualOrganUtils().has_penis(sim_info):
                DDPenisStateUtils().set_flaccid(sim_info, update_outfit=True)
            elif DDNuditySystemUtils().has_strapon_equipped(sim_info):
                DDNuditySystemUtils().remove_strapon(sim_info)
        except Exception as e:
            log.error("Error", exception=e, throw=True)

    def set_sim_penis_state(self, sim_info: SimInfo, cmd: str, _sim_id: str, _state: str, _duration: str = '0', _update_outfit: str = 'False', _reason: str = None):
        try:
            if _state == 'True':
                state = True
            else:
                state = False
            duration = int(_duration)
            if _update_outfit == 'True':
                update_outfit = True
            else:
                update_outfit = False

            if duration > 0:
                # try to set the duration to a reasonable value (add 30 to it)
                self.run_after.add(30 + duration, f'ww.execute {cmd} {_sim_id} {not state} 0 {update_outfit}')

            reason = DDSexSystemStringId.HAVE_SEX

            log.debug(f"Called(2): {cmd} '{sim_info}' {state} {duration} {update_outfit}")
            if DCSexualOrganUtils().has_penis(sim_info):
                if state:
                    DDPenisStateUtils().set_erect(sim_info, reason, update_outfit=update_outfit)
                else:
                    DDPenisStateUtils().set_flaccid(sim_info, update_outfit=update_outfit)
            else:
                # Sim has no penis, this should never be called. Don't assume that the sim wants to wear a strap-on.
                if update_outfit:
                    if state:
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE)
                    else:
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.UNDERWEAR)

        except Exception as e:
            log.error("Error", exception=e, throw=True)
