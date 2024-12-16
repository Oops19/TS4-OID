#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


class VanillaFunction:

    F_IMPREGNATE = 'bg_impregnate'  # sim gets pregnant

    # TODO - Everything below to be implemented

    F_HAS_TRAIT = 'bg_has_trait'  # trait name or ID, exit if trait is missing
    F_ADD_TRAIT = 'bg_add_trait'
    F_ADD_BUFF = 'bg_add_buff'

    F_ADD_VFX = 'bg_play_vfx'  # (id, bone, vfx-name)  # id=1-1000 to identify the effect. bone=bone name # TODO figure out best way to support chars in (...)
    # currently only '1-9,.' are supported. TODO
    F_STOP_VFX = 'bg_stop_vfx'  # (id)

    # Outfit related functions - BG
    F_UNDO_OUTFIT = 'bg_undo_outfit'

    F_UNDRESS_PREFIX = 'bg_undress_'
    F_EQUIP_PREFIX = 'bg_equip_'
    F_UNDRESS_CAS_PARTS = 'bg_undress_cas_parts'  # append (1-3,8-10) - the body parts to remove, (1-200) to remove everything incl. tattoos, scars, makeup, rings, ...
    F_EQUIP_CAS_PARTS = 'bg_equip_cas_parts'  # append (1-3, 8-10, HAT) - these body parts will be to added

    F_EQUIP_ALL = 'bg_equip_all'
    F_EQUIP_FULL = 'bg_equip_full'
    F_EQUIP_TOP = 'bg_equip_top'
    F_EQUIP_BOTTOM = 'bg_equip_bottom'
    # F_EQUIP_SHOES = 'bg_equip_shoes'
    # F_EQUIP_NEXT = 'bg_equip_next'  # add 1 cas part in a pre-defined order (... SHOE, HAT)

    F_UNDRESS_ALL = 'bg_undress_all'  # Undo: 'undress_bottom' - all outfit/garment odyParts will be added by p_equip_all
    F_UNDRESS_FULL = 'bg_undress_full'
    F_UNDRESS_TOP = 'bg_undress_top'  # Undo: p_wear_top
    F_UNDRESS_BOTTOM = 'bg_undress_bottom'  # Undo: p_wear_bottom
    F_UNDRESS_SHOES = 'bg_undress_shoes'
    F_UNDRESS_NEXT = 'bg_undress_next'  # remove 1 cas part in a pre-defined order (HAT, SHOE, ...)