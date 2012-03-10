from __future__ import print_function
import sys
import mudlib.rooms
import mudlib.player
import mudlib.races
import mudlib.soul
import mudlib.util
import mudlib.baseobjects
import mudlib.errors
import mudlib.cmds

def create_player_from_info():
    while True:
        name = raw_input("Name? ").strip()
        if name:
            break
    gender = raw_input("Gender m/f/n? ").strip()[0]
    while True:
        print("Player races:", ", ".join(mudlib.races.player_races))
        race = raw_input("Race? ").strip()
        if race in mudlib.races.player_races:
            break
        print("Unknown race, try again.")
    wizard = raw_input("Wizard y/n? ").strip() == "y"
    description = "This is a random mud player."
    player = mudlib.player.Player(name, gender, race, description)
    if wizard:
        player.privileges.add("wizard")
        player.set_title("arch wizard %s", includes_name_param=True)
    return player

def create_default_wizard():
    player = mudlib.player.Player("irmen", "m", "human", "This wizard looks very important.")
    player.privileges.add("wizard")
    player.set_title("arch wizard %s", includes_name_param=True)
    return player

def create_default_player():
    player = mudlib.player.Player("irmen", "m", "human", "A regular person.")
    return player


class Commands(object):
    def __init__(self):
        self.commands_per_priv = {None: {}}

    def add(self, verb, func, privilege):
        self.commands_per_priv.setdefault(privilege, {})[verb] = func

    def get(self, privileges):
        result = self.commands_per_priv[None]  # always include the cmds for None
        for priv in privileges:
            if priv in self.commands_per_priv:
                result.update(self.commands_per_priv[priv])
        return result


class Driver(object):
    def __init__(self):
        self.player = None
        self.commands = Commands()
        mudlib.cmds.register_all(self.commands)

    def start(self, args):
        # print GPL 3.0 banner
        print("\nSnakepit mud driver and mudlib. Copyright (C) 2012  Irmen de Jong.")
        print("This program comes with ABSOLUTELY NO WARRANTY. This is free software,")
        print("and you are welcome to redistribute it under the terms and conditions")
        print("of the GNU General Public License version 3. See the file LICENSE.txt")
        # print MUD banner and initiate player creation
        print("\n" + mudlib.MUD_BANNER + "\n")
        choice = raw_input("Create default (w)izard, default (p)layer, (c)ustom player? ").strip()
        if choice == "w":
            player = create_default_wizard()
        elif choice == "p":
            player = create_default_player()
        else:
            player = create_player_from_info()
        self.player = player
        self.move_player_to_start_room()
        self.player.tell("\nWelcome to %s, %s.\n\n" % (mudlib.MUD_NAME, self.player.title))
        self.player.tell(self.player.look())
        self.main_loop()

    def move_player_to_start_room(self):
        if "wizard" in self.player.privileges:
            self.player.move(mudlib.rooms.STARTLOCATION_WIZARD)
        else:
            self.player.move(mudlib.rooms.STARTLOCATION_PLAYER)

    def main_loop(self):
        print = self.player.tell
        keep_going = True
        while keep_going:
            mudlib.mud_context.driver = self
            mudlib.mud_context.player = self.player
            self.write_output()
            try:
                keep_going = self.ask_player_input()
            except mudlib.soul.UnknownVerbException, x:
                if x.verb in ("north", "east", "south", "west", "up", "down"):
                    print("You can't go in that direction.")
                else:
                    print("The verb %s is unrecognised." % x.verb)
            except (mudlib.errors.ParseError, mudlib.errors.ActionRefused), x:
                print(str(x))
            except Exception:
                import traceback
                print("* internal error:")
                print(traceback.format_exc())
        self.write_output()

    def write_output(self):
        # print any buffered player output
        output = self.player.get_output_lines()
        print("".join(output))

    def ask_player_input(self):
        cmd = raw_input(">> ")
        verb, _, rest = cmd.partition(" ")
        verb = verb.strip()
        rest = rest.strip()
        # determine available verbs for this player
        player_verbs = self.commands.get(self.player.privileges)
        # pre-process input special cases
        if verb.startswith("'"):
            verb = "say"
            rest = cmd[1:].strip()
            cmd = "say " + rest
        elif verb in mudlib.cmds.abbreviations:
            verb = mudlib.cmds.abbreviations[verb]
            cmd = verb + " " + rest
        # Execute. First try directions, then the rest
        if verb in self.player.location.exits:
            self.do_move(verb)
            return True
        elif verb in player_verbs:
            func = player_verbs[verb]
            result = func(self.player, verb, rest, driver=self, verbs=player_verbs)
            return result != False
        else:
            self.do_socialize(cmd)
            return True

    def do_move(self, direction):
        exit = self.player.location.exits[direction]
        if not exit.bound:
            # resolve the location and replace with bound Exit
            target_module, target_object = exit.target.rsplit(".", 1)
            module = mudlib.rooms
            for name in target_module.split("."):
                module = getattr(module, name)
            target = getattr(module, target_object)
            # note: could be more than one occurrence for 1 exit (an alias)
            #exits = [ d for d,e in self.player.location.exits.items() if e is exit ]
            #exit = mudlib.baseobjects.Exit(target, exit.description)
            #for d in exits:
            #    self.player.location.exits[d] = exit
            exit.bind(target)
        exit.allow(self.player)
        self.player.move(exit.target)
        self.player.tell(self.player.look())

    def do_socialize(self, cmd):
        player = self.player
        verb, (who, player_message, room_message, target_message) = player.socialize(cmd)
        player.tell(player_message)
        player.location.tell(room_message, player, who, target_message)
        if verb in mudlib.soul.AGGRESSIVE_VERBS:
            # usually monsters immediately attack,
            # other npcs may choose to attack or to ignore it
            for living in who:
                if living.aggressive:
                    living.start_attack(self.player)

    def search_player(self, name):
        """Look through all the logged in players for one with the given name"""
        if self.player.name == name:
            return self.player
        return None


if __name__ == "__main__":
    driver = Driver()
    driver.start(sys.argv[1:])
