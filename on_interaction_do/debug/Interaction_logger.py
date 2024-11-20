#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Set, Union

from interactions.base.interaction import Interaction
from on_interaction_do.modinfo import ModInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_pre_run import S4CLInteractionPreRunEvent
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)


class InteractionLogger(metaclass=Singleton):
    def __init__(self):
        self.sim_ids: Set[int] = set()
        self.sim_pre_ids: Set[int] = set()


    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.debug.log', 'Log all interactions.')
    def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
        # output is already provided
        try:
            il = InteractionLogger()
            sim_id = CommonSimUtils.get_active_sim_id()
            sim_info = CommonSimUtils.get_active_sim_info()
            if sim_id in il.sim_ids:
                il.sim_ids.remove(sim_id)
                output(f"Disabled interaction log for {sim_info}")
            else:
                il.sim_ids.add(sim_id)
                output(f"Enabled interaction log for {sim_info}")
        except Exception as e:
            log.error(f"Oops: {e}", throw=True)

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.debug.log_pre_run', 'Log all interactions when they get added.')
    def o19_cheat_log_all_pre_interactions(output: CommonConsoleCommandOutput):
        # output is already provided
        try:
            il = InteractionLogger()
            sim_id = CommonSimUtils.get_active_sim_id()
            sim_info = CommonSimUtils.get_active_sim_info()
            if sim_id in il.sim_pre_ids:
                il.sim_pre_ids.remove(sim_id)
                output(f"Disabled pre-run interaction log for {sim_info}")
            else:
                il.sim_pre_ids.add(sim_id)
                output(f"Enabled pre-run interaction log for {sim_info}")
        except Exception as e:
            log.error(f"Oops: {e}", throw=True)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_pre_run_event(event_data: S4CLInteractionPreRunEvent) -> bool:
        try:
            InteractionLogger().filter_queued_event('PreRun', event_data)
            return True
        except Exception as ex:
            log.error("Error: " + str(ex))

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_pre_run_event(event_data: S4CLInteractionQueuedEvent) -> bool:
        try:
            InteractionLogger().filter_queued_event('Queued', event_data)
            return True
        except Exception as ex:
            log.error("Error: " + str(ex))

    def filter_queued_event(self, queue_name: str, event_data: Union[S4CLInteractionPreRunEvent, S4CLInteractionQueuedEvent]):
        sim_id = event_data.interaction_queue.sim.sim_id
        if sim_id in self.sim_ids or sim_id in self.sim_pre_ids:
            sim_info = CommonSimUtils.get_sim_info(sim_id)
            try:
                source = event_data.interaction.source
            except:
                source = ''
            try:
                interaction_name = CommonInteractionUtils.get_interaction_short_name(event_data.interaction)
            except:
                interaction_name = ''
            try:
                interaction_id = CommonInteractionUtils.get_interaction_id(event_data.interaction)
            except:
                interaction_id = -1
            if ((sim_id in self.sim_ids and f"{event_data.event_name}" == "S4CLInteractionQueuedEvent") or
                    (sim_id in self.sim_pre_ids and f"{event_data.event_name}" == "S4CLInteractionPreRunEvent")):
                log.debug(f"q={queue_name} sim='{sim_info}' source='{source}' interaction='{event_data.interaction}'")
                log.debug(f"q={queue_name} sim='{sim_id}' source='{source}' interaction='{interaction_name} ({interaction_id})'")
