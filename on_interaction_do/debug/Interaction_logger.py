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
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)


class InteractionLogger(metaclass=Singleton):
    def __init__(self):
        self.sim_ids: Set[int] = set()

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_pre_run_event(event_data: S4CLInteractionPreRunEvent) -> bool:
        try:
            InteractionLogger().filter_queued_event('S4CLInteractionPreRunEvent', event_data)
            return True
        except Exception as ex:
            log.error("Error: " + str(ex))

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_pre_run_event(event_data: S4CLInteractionQueuedEvent) -> bool:
        try:
            InteractionLogger().filter_queued_event('S4CLInteractionQueuedEvent', event_data)
            return True
        except Exception as ex:
            log.error("Error: " + str(ex))

    def filter_queued_event(self, queue_name: str, event_data: Union[S4CLInteractionPreRunEvent, S4CLInteractionQueuedEvent]):
        sim_id = event_data.interaction_queue.sim.sim_id
        if sim_id not in self.sim_ids:
            return
        try:
            source = event_data.interaction.source
        except:
            source = ''

        log.debug(f"q={event_data.event_name} sim_id='{sim_id}' source='{source}' interaction='{event_data.interaction.guid} {event_data.interaction}'")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.log_interactions', 'Log all interactions.')
def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
    # output is already provided
    try:
        il = InteractionLogger()
        sim_id = CommonSimUtils.get_active_sim_id()
        if sim_id in il.sim_ids:
            il.sim_ids.remove(sim_id)
            output(f"Disabled logging for {sim_id}")
        else:
            il.sim_ids.add(sim_id)
            output(f"Enabled logging for {sim_id}")
    except Exception as e:
        log.error(f"Oops: {e}", throw=True)
