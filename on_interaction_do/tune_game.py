#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Dict, Union, List

from on_interaction_do.cache.data_store import DataStore
from on_interaction_do.cache.init_cache import InitCache
from on_interaction_do.enums.oid_constants import OidConstants
from on_interaction_do.modinfo import ModInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.utils.basic_extras import BasicExtras
from ts4lib.utils.tuning_helper import TuningHelper

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class TuneGame:
    def __init__(self, user_data: Dict):
        self.user_data = user_data
        self.tuning_helper: TuningHelper = TuningHelper()  # Singleton
        self.basic_extras: BasicExtras = BasicExtras()  # Singleton

    def process_user_data(self):
        for name, data in self.user_data.items():
            log.debug(f"Processing '{name}'")
            _filter: Union[Dict, None] = data.get('filter', None)
            actions: Union[Dict, None] = data.get('actions', None)
            commands: List[str, None] = data.get('commands', None)
            if _filter is None or actions is None:
                continue
            cmd = _filter.get('command', OidConstants.COMMAND)  # default 'o19.tuning.commands'
            manager: str = _filter.get('manager', OidConstants.TUNING)  # default 'INTERACTION',
            tunings: List[str] = _filter.get('tunings')  # eg ["baby_Mixer_BabyFeed_Body_Succeed", ],
            tuning_ids = self.tuning_helper.get_tuning_ids(manager, tunings)

            for action_name, action in actions.items():
                log.debug(f"... processing {action_name}")
                param = '+'.join(action.get('parameters', ''))  # eg 'undress+milk' from ['undress', 'milk', ]
                if not param:
                    continue
                if 'tunings_ref' in param:
                    tunings_ref = DataStore().store_interaction_ids(tuning_ids)
                    param = param.replace('tunings_ref', f"{tunings_ref}")
                timing = action.get('timing', OidConstants.TIMING_AT_END)
                offset_time = action.get('offset_time', None)
                xevt_id = action.get('xevt_id', None)
                drop_all_basic_extras = action.get('drop_all_basic_extras', False)
                drop_basic_extras = action.get('drop_basic_extras', None)
                include_target_sim = action.get('include_target_sim', True)
                include_target_object = action.get('include_target_object', False)

                self.basic_extras.add_do_command(
                    manager, tuning_ids, cmd, param,
                    timing=timing, offset_time=offset_time, xevt_id=xevt_id,
                    drop_all_basic_extras=drop_all_basic_extras,
                    drop_basic_extras=drop_basic_extras,
                    include_target_sim=include_target_sim,
                    include_target_object=include_target_object
                )
            if commands:
                for command in commands:
                    if command == 'remove_privacy':
                        tuning_dict = self.tuning_helper.get_tuning_dict(manager, tuning_ids)
                        self.tuning_helper.remove_privacy(tuning_dict)

    def start(self):
        log.debug("# User Config START")
        self.process_user_data()
        log.debug("# User Config END")

    # noinspection PyUnusedLocal
    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def o19_handle_event(event_data: S4CLZoneLateLoadEvent):  # S4CLZoneEarlyLoadEvent
        ic = InitCache()
        if ic.vanilla is False:
            # TuneBaseGame.start()  # TODO add stuff to config file and read it
            ic.vanilla = True
