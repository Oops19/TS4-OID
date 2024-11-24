#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


class GenericFunction:
    # F_ = function_
    # P_ = parameter_

    ID = 'id'
    NOP = 'nop'
    JOIN = '+'

    F_REPEAT = 'g_repeat'  # append (tunings_ref, 0-999,0-99)  # tunings_ref references the tunings, t_max to repeat the command for this sim, delay between repeats
    # Everything behind this command will be repeated.

    F_RANDOM = 'g_random'  # g_random(p) for a p% success change to continue (range: 1-99) with the next command
    RANDOM_DEFAULT_VALUE: int = 50

    # rotate 5° every 3 seconds or so. Both values are hard-coded currently
    F_ROTATE_ABS = 'g_rotate_abs'  # append (0-360) to rotate the sim (270° will be converted to -90°)
    F_ROTATE_RND = 'g_rotate_rnd'  # append (0-360,0-180) set 1st value to '50' and second value to '10' to rotate the sim to 40°-60°
    F_ROTATE_END = 'g_rotate_end'  # end rotation early (to avoid rotation after end of the interaction)

    F_OPACITY = 'g_opacity'  # append (0-1,0-99) - float values for opacity and fade duration

    """
    g_repeat(n: int, t_max: int = 10_000, t_delay: int = 60)  n as Tuning Reference, t_max for the maximum time, t_delay between repeats
    The current sim will repeatedly execute the remaining functions after `g_repeat(...)+`
    * n: n=DataStore.store_interaction_ids([tuning_ids, ]) - As long as one of these interactions (tunings) is running the functions will be repeated
    * n: n=0 - The functions will be repeated until t_max has been reached
    """
    REPEAT_DEFAULT_VALUE_T_MAX: float = 10_000.0
    REPEAT_DEFAULT_VALUE_T_DELAY: float = 60.0

    """
    Debugging
    Use the log file for an accurate time stamp.
    It can be handy to show a popup when an animation starts. E.g. ALERT for start and INFO for the end of the interaction.
    """
    F_DEBUG_INFO = 'g_debug_info'  # append (1) to show a blue info popup notification in-game with value '1' (supported characters within () are "1-9,.")
    F_DEBUG_ALERT = 'g_debug_alert'  # append (1) to show an orange warning popup notification in-game with value '1' (supported characters within () are "1-9,.")

    """
    Outfit related functions. They usually start with 's_' and will be executed by DC or BG.
    """

    F_UNDO_OUTFIT = 's_undo_outfit'  # Restore the current outfit for undo operation. Should never be placed after commands which modify the outfit.
    # append (0-999)  # Undo t_max seconds after starting the command
    # append (0-999,1-900)  # + Wait 1-900 after the interaction ends.
    # TODO append (0-999,1-900, {min_interaction_id},{max_interaction_id})  # Undo earlier as soon as no interaction_id within the range is running.

    """
    Generic equip and undress functions call either the bg_ or the dc_ functions.
    They should be used so the mod can decide what function to use.
    Unless there is a reason to limit functionality to BG or DC.
    """
    F_UNDRESS_CAS_PARTS = 's_undress_cas_parts'  # append (5, 6, 7) - the body parts to remove
    F_EQUIP_CAS_PARTS = 's_equip_cas_parts'  # append (1, 2, 3, 8, 9, 10) - these body parts will be to added

    F_EQUIP_ALL = 's_equip_all'
    F_EQUIP_FULL = 's_equip_full'
    F_EQUIP_TOP = 's_equip_top'
    F_EQUIP_BOTTOM = 's_equip_bottom'
    # F_EQUIP_SHOES = 's_equip_shoes'
    # F_EQUIP_NEXT = 's_equip_next'  # add 1 cas part in a pre-defined order (... SHOE, HAT)

    F_UNDRESS_ALL = 's_undress_all'  # Undo: 'undress_bottom' - all outfit/garment odyParts will be added by p_equip_all
    F_UNDRESS_FULL = 's_undress_full'
    F_UNDRESS_TOP = 's_undress_top'  # Undo: p_wear_top
    F_UNDRESS_BOTTOM = 's_undress_bottom'  # Undo: p_wear_bottom
    F_UNDRESS_SHOES = 's_undress_shoes'

    F_UNDRESS_NEXT = 's_undress_next'  # s_undress_next: Remove 1 cas part in a pre-defined order.
                                       # TODO s_underss_next(1,2,3): Remove 1 cas part of these in a pre-defined order.


    # TODO
    P_SELECT_ACTOR_SIM = 'g_select_actor_sim'  # The default
    P_SELECT_TARGET_SIM = 'g_select_target_sim'  # Not set for all interactions