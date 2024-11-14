#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from ts4lib.utils.singleton import Singleton


class InitCache(object, metaclass=Singleton):
    def __init__(self):
        self._kritical = False
        self._vanilla = False
        self._userconf = False
        self._wwcheats = False

    @property
    def kritical(self) -> bool:
        return self._kritical

    @kritical.setter
    def kritical(self, i):
        self._kritical = i

    @property
    def vanilla(self) -> bool:
        return self._vanilla

    @vanilla.setter
    def vanilla(self, i):
        self._vanilla = i

    @property
    def userconf(self) -> bool:
        return self._userconf

    @userconf.setter
    def userconf(self, i):
        self._userconf = i

    @property
    def wwcheats(self) -> bool:
        return self._wwcheats

    @wwcheats.setter
    def wwcheats(self, i):
        self._wwcheats = i
