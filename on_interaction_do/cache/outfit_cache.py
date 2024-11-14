#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import List, Dict

from ts4lib.utils.singleton import Singleton


class OutfitCache(object, metaclass=Singleton):
    """
    Store sim_info: [is_nude, is_under, is_strap], eg: 123: [False, False, False]
    """
    outfit_top: Dict[int, List[bool]] = dict()
    outfit_bottom: Dict[int, List[bool]] = dict()
