"""
Package containing the mob classes of the game.

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

import random
from tale.base import Living
from tale.util import Context

__all__ = ("CircleMob", "MPostmaster", "MCityguard", "MReceptionist", "MCryogenicist", "MFido",
           "MGuild", "MGuildguard", "MJanitor", "MMagicuser", "MMayor", "MPuff", "MSnake", "MThief",
           "MGuildguard_Cleric", "MGuildguard_Mage", "MGuildguard_Thief", "MGuildguard_Warrior",
           "MGuildmaster_Cleric", "MGuildmaster_Mage", "MGuildmaster_Thief", "MGuildmaster_Warrior",
           "MCastleGuard", "MJames", "MCleaning", "MDicknDavid", "MJerry", "MKingWelmar",
           "MPeter", "MTim", "MTom", "MTrainingMaster")


class CircleMob(Living):
    """Monster NPC having tailored behavior to suit circle data"""
    def init(self) -> None:
        super().init()

    def do_wander(self, ctx: Context) -> None:
        # Let the mob wander randomly. Note: not all mobs do this!
        direction = self.select_random_move()
        if direction:
            self.move(direction.target, self)
        ctx.driver.defer(random.randint(20, 60), self.do_wander)


# @todo implement the behavior of the various mob classes (see spec_procs.c / castle.c)

class MPostmaster(CircleMob):
    pass


class MCityguard(CircleMob):
    pass


class MReceptionist(CircleMob):
    pass


class MCryogenicist(CircleMob):
    pass


class MGuildguard(CircleMob):
    pass


class MGuild(CircleMob):
    pass


class MPuff(CircleMob):
    pass


class MFido(CircleMob):
    pass


class MJanitor(CircleMob):
    pass


class MMayor(CircleMob):
    pass


class MSnake(CircleMob):
    pass


class MThief(CircleMob):
    pass


class MMagicuser(CircleMob):
    pass


class MGuildmaster_Mage(CircleMob):      # @todo MGuild?
    pass


class MGuildmaster_Cleric(CircleMob):
    pass


class MGuildmaster_Warrior(CircleMob):
    pass


class MGuildmaster_Thief(CircleMob):
    pass


class MGuildguard_Mage(CircleMob):
    pass


class MGuildguard_Cleric(CircleMob):
    pass


class MGuildguard_Warrior(CircleMob):
    pass


class MGuildguard_Thief(CircleMob):
    pass


# mobs from the Castle zone (150): (see castle.c)

class MCastleGuard(CircleMob):
    pass


class MJames(CircleMob):
    pass


class MCleaning(CircleMob):
    pass


class MDicknDavid(CircleMob):
    pass


class MTim(CircleMob):
    pass


class MTom(CircleMob):
    pass


class MKingWelmar(CircleMob):
    pass


class MTrainingMaster(CircleMob):
    pass


class MPeter(CircleMob):
    pass


class MJerry(CircleMob):
    pass