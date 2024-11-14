#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import time
from typing import Dict, Set, List
import services

import sims4
import sims4.commands
from on_interaction_do.modinfo import ModInfo

from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class RunAfter(object, metaclass=Singleton):
    queue: Dict[float, List] = {}
    unique_queue_items: Set[int] = set()

    @staticmethod
    def add(duration: int, command: str, uid: int = -1):
        if uid > 0 and uid in RunAfter.unique_queue_items:
            return
        t = time.time() + duration
        RunAfter.queue.update({t + duration: [uid, command]})
        log.debug(f"    Enqueue({duration}): {command}")

    @staticmethod
    def _loop():
        remove_times = set()
        t = time.time()
        for run_after, uid_command in RunAfter.queue.items():
            if run_after < t:
                uid, command = uid_command
                log.debug(f"Running: {command}")
                remove_times.add(run_after)
                # noinspection PyBroadException
                try:
                    RunAfter.unique_queue_items.remove(uid)
                except:
                    pass
                try:
                    sims4.commands.execute(command, RunAfter()._client_id())
                except Exception as e:
                    log.error("Error", exception=e, throw=True)
        for remove_time in remove_times:
            del RunAfter.queue[remove_time]

    @staticmethod
    def _client_id() -> int:
        # noinspection PyBroadException
        try:
            return services.client_manager().get_first_client().id
        except:
            return 1

    @staticmethod
    @CommonIntervalEventRegistry.run_every(ModInfo.get_identity(), milliseconds=5_000)
    def o19_run_after_timer():
        if CommonTimeUtils.game_is_paused():
            return
        RunAfter()._loop()
