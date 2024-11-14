#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#

class OidConstants:
    COMMAND = 'o19.oid.do_command'  # default command, access the value with OidConstants.COMMAND
    TUNING = "INTERACTION"  # default interaction
    RUN_COMMAND = 'o19.oid.run'

    PREFIX_GENERIC = 'g_'
    PREFIX_DC_OR_VANILLA = 's_'
    PREFIX_VANILLA = 'bg_'
    PREFIX_DC = 'dc_'

    # do_command parameters
    OPT_TIMING = 'timing'  # 'timing': 'at_end',  # default; str;  supported values: at_beginning, at_end
    OPT_OFFSET_TIME = 'offset_time'  # 'offset_time': None,  # default; float; delay starting the command
    OPT_XEVT_ID = 'xevt_id'  # 'xevt_id': None,  # default, int;  execute the command when a xevt_id occurs
    OPT_DROP_ALL_BASIC_EXTRAS = 'drop_all_basic_extras'  # 'drop_all_basic_extras': False,  # default; bool; True drops all basic_extras of the tuning (interaction)
    OPT_DROP_BASIC_EXTRAS = 'drop_basic_extras'  # 'drop_basic_extras': None,  # default; List[str]; Individual classes to drop
    OPT_INCLUDE_TARGET_SIM = 'include_target_sim'  # 'include_target_sim': True,  # default; bool; Set to 'False' to omit the target sim

    # do_command parameter values
    TIMING_AT_BEGINNING = 'at_beginning'
    TIMING_AT_END = 'at_end'
    TIMING_ON_XEVT = 'on_xevt'

