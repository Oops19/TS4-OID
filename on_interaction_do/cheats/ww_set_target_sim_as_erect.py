#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from on_interaction_do.cheats.do_ww_command import DoWwCommand
from on_interaction_do.modinfo import ModInfo
from sims4.commands import CommandType, Command

from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils

from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


@Command('ww.set_target_sim_as_erect', command_type=CommandType.Live, )
def cmd_o19_cheat_ww_set_target_sim_as_erect(*args, _connection=None):
    log.debug(f"Called(1): ww.set_target_sim_as_erect {args}")
    try:
        _args = ''
        for arg in args:
            _args = f"{_args} '{arg}:{type(arg)}'"
        _sim_id = f"{args[0]}"
        sim_id = int(_sim_id)
        sim_info = CommonSimUtils.get_sim_info(sim_id)
        dwc = DoWwCommand()

        unknown_interaction: bool = True
        for interaction in CommonSimInteractionUtils.get_running_interactions_gen(sim_info):
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            interaction_name = CommonInteractionUtils.get_interaction_short_name(interaction)
            if interaction_id in dwc.unsupported_interactions:
                log.debug(f"\tInteraction '{interaction_name}' not supported.")
                return
            if interaction_id in dwc.supported_interactions:
                unknown_interaction = False
                break
        if unknown_interaction:
            log.warn(f"\tNew / unknown interaction. Hopefully it works properly.")

        dwc.set_sim_penis_state(sim_info, '- (ww.set_target_sim_as_erect)', _sim_id, 'True', )
    except Exception as e:
        log.error(f"Oops: '{e}'")
