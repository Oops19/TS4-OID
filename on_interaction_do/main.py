#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Union

from on_interaction_do.cache.init_cache import InitCache
from on_interaction_do.cheats.do_ww_command import DoWwCommand
from on_interaction_do.modinfo import ModInfo
from on_interaction_do.tune_game import TuneGame
from on_interaction_do.user_config import UserConfig
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()
log.debug(f"Starting {ModInfo.get_identity().name} v{ModInfo.get_identity().version} ")


class Main:

    def __init__(self):
        self.uc: Union[UserConfig, None] = None
        self.ic: Union[InitCache, None] = None

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def o19_handle_event(event_data: S4CLZoneLateLoadEvent):
        uc = UserConfig()  # Singleton
        log.debug(f"{uc.configuration_data}")
        ic = InitCache()  # Singleton

        # Initialize interactions specified by user
        if ic.userconf is False:
            tg = TuneGame(uc.configuration_data)
            tg.start()
            ic.userconf = True

        # Initialize ww cheat commands
        if ic.wwcheats is False:
            DoWwCommand()
            ic.wwcheats = True
