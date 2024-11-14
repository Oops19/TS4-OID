#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Union, Any

import services
import sims4
import sims4.resources

from native.animation import NativeAsm
from on_interaction_do.modinfo import ModInfo
from on_interaction_do.tune_game import TuneGame
from on_interaction_do.tune_kritical import TuneKritical
from on_interaction_do.user_config import UserConfig
from sims.sim import Sim
from sims4.hash_util import hash64
from sims.sim_info import SimInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.tuning_helper import TuningHelper


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.run_kritical', "Re-run 'Kritical'")
def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
    th = TuningHelper()
    th.verbose = True
    TuneKritical.start()
    th.verbose = False
    output(f"Done")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.run_vanilla', "Re-run 'Vanilla'")
def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
    th = TuningHelper()
    th.verbose = True
    uc = UserConfig()
    user_data = uc.configuration_data
    TuneGame(user_data).start()
    th.verbose = False
    output(f"Done")

    rt_manager = "INTERACTION"
    instance_manager = services.get_instance_manager(sims4.resources.Types[rt_manager])
    output(f"{instance_manager}")
    i = 0
    tuning_name = '_PillowFight_Target'
    tuning_name = tuning_name.lower().strip()
    for (key, tuning_file) in instance_manager.types.items():
        if i < 20:
            i += 1
            output(f"{tuning_file.__name__.lower()}")
        if f"{tuning_file.__name__.lower()}".endswith(tuning_name):
            output(f"XX {tuning_file.__name__.lower()}")

@CommonConsoleCommand(ModInfo.get_identity(), 'o19.critical.feet', 'Undress shoes.')
def cmd_o19_kri_feet(output: CommonConsoleCommandOutput):
    def _setup_asm_default(self, interaction_sim: Sim, interaction_target: Any, interaction_asm: NativeAsm, *args, **kwargs) -> Union[bool, None]:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
        equipment_part_handle = DDNuditySystemUtils().get_equipment_part_handle_from_handle_type(self.part_handle)
        current_layer = equipment_part_handle.get_current_layer(target_sim_info)
        interaction_asm.set_parameter('current_undress_layer', current_layer.name.lower())
        interaction_asm.set_parameter('to_undress_layer', self.to_layer.name.lower())
        # We return None here to indicate that we do not want to replace the original asm.
        return None

    try:
        sim_info: SimInfo = CommonSimUtils.get_active_sim_info()
        sim: Sim = CommonSimUtils.get_sim_instance(sim_info)
        # interaction_asm: NativeAsm = None
        # _setup_asm_default(sim, sim, interaction_asm)

        anim_prefix = 'GEN_DeviousDesires_Nudity_Interaction_ModifyEquipment_ByPartHandleAnimated'
        undress_anim = 'NUDE_EQUIPMENT_FEET'
        interaction_id = hash64(f"{anim_prefix}_{undress_anim}")
        high_value = 1 << (64 - 1)
        interaction_id = interaction_id | high_value
        output(f"{sim_info}: {interaction_id}")
        result = CommonSimInteractionUtils.queue_interaction(sim_info, interaction_id, target=sim)
        output(f"OK {result}")
    except Exception as e:
        output(f"Oops: {e}")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gender', 'Whatever.')
def cmd_o19_gender_info(output: CommonConsoleCommandOutput):
    try:
        output(f"O")
        sim_info: SimInfo = CommonSimUtils.get_active_sim_info()
        output(f"M={CommonGenderUtils.is_male(sim_info)} F={CommonGenderUtils.is_female(sim_info)}")
    except Exception as e:
        output(f"Oops: {e}")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.layerinfo', 'Whatever.')
def cmd_o19_layer_info(output: CommonConsoleCommandOutput):
    try:
        from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
        from deviousdesires.nudity_system.enums.part_handle_type import DDPartHandleType
        from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
        sim_info: SimInfo = CommonSimUtils.get_active_sim_info()
        parts = (DDPartHandleType.EQUIPMENT_TOP, DDPartHandleType.EQUIPMENT_BOTTOM, DDPartHandleType.EQUIPMENT_SOCKS, DDPartHandleType.EQUIPMENT_FEET,
                 DDPartHandleType.EQUIPMENT_FULL_BODY, DDPartHandleType.EQUIPMENT_CUMMERBUND,)
        for undress_part in parts:
            is_outerwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.OUTERWEAR).result
            is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
            is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
            output(f"{undress_part}: {is_outerwear}|{is_underwear}|{is_nude}")

        output(f"OK")
    except Exception as e:
        output(f"Oops: {e}")
