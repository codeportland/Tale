import unittest
from mudlib.baseobjects import Location, Exit, Item
from mudlib.npc import NPC
from mudlib.player import Player

hall = Location("Main hall", "A very large hall.")
attic = Location("Attic", "A dark attic.")
street = Location("Street", "An endless street.")
hall.exits["up"] = Exit(attic, "A ladder leads up.")
hall.exits["door"] = Exit(street, "A heavy wooden door to the east blocks the noises from the street outside.")
hall.exits["east"] = hall.exits["door"]
hall.items.update({
    Item("table", "oak table", "a large dark table with a lot of cracks in its surface"),
    Item("key", "rusty key", "an old rusty key without a label"),
    Item("magazine", "university magazine")
    })
rat, julie = NPC("rat", "n", race="rodent"), NPC("julie", "f", "attractive Julie",
                                 """
                                 She's quite the looker.
                                 """)
hall.livings = { rat, julie }


class TestLocations(unittest.TestCase):
    def test_look(self):
        expected = """[Main hall]
A very large hall.
You see an oak table, a rusty key, and a university magazine.
A heavy wooden door to the east blocks the noises from the street outside.
A ladder leads up.
Attractive Julie and rat are here."""
        self.assertEqual(expected, hall.look())
        expected = """[Attic]
A dark attic."""
        self.assertEqual(expected, attic.look())

    def test_look_short(self):
        expected = """[Attic]"""
        self.assertEqual(expected, attic.look(short=True))
        expected = """[Main hall]
You see: key, magazine, table
Exits: door, east, up
Present: julie, rat"""
        self.assertEqual(expected, hall.look(short=True))
        expected = """[Main hall]
You see: key, magazine, table
Exits: door, east, up
Present: rat"""
        self.assertEqual(expected, hall.look(exclude_living=julie, short=True))

    def test_search_living(self):
        self.assertEquals(None, hall.search_living("<notexisting>"))
        self.assertEquals(None, attic.search_living("<notexisting>"))
        self.assertEquals(rat, hall.search_living("rat"))
        self.assertEquals(julie, hall.search_living("Julie"))
        self.assertEquals(julie, hall.search_living("attractive julie"))

    def test_tell(self):
        class MsgTraceNPC(NPC):
            def __init__(self, name, gender, race):
                super(MsgTraceNPC, self).__init__(name, gender, race=race)
                self.clearmessages()
            def clearmessages(self):
                self.messages = []
            def tell(self, *messages):
                self.messages.extend(messages)
        rat = MsgTraceNPC("rat", "n", "rodent")
        julie = MsgTraceNPC("julie", "f", "human")
        hall = Location("hall")
        hall.livings = [rat, julie]
        hall.tell("roommsg")
        self.assertEqual(["roommsg"], rat.messages)
        self.assertEqual(["roommsg"], julie.messages)
        rat.clearmessages()
        julie.clearmessages()
        hall.tell("roommsg", rat, [julie], "juliemsg")
        self.assertEqual([], rat.messages)
        self.assertEqual(["juliemsg"], julie.messages)


class TestNPC(unittest.TestCase):
    def test_init(self):
        self.assertEqual("julie", julie.name)
        self.assertEqual("attractive Julie", julie.title)
        self.assertEqual("She's quite the looker.", julie.description)
        self.assertEqual("human", julie.race)
        self.assertEqual("f", julie.gender)
        self.assertTrue(1 < julie.stats["agi"] < 100)
        self.assertEqual("rat", rat.name)
        self.assertEqual("rat", rat.title)
        self.assertEqual("rodent", rat.race)
        self.assertEqual("", rat.description)
        self.assertEqual("n", rat.gender)
        self.assertTrue(1 < rat.stats["agi"] < 100)


class TestPlayer(unittest.TestCase):
    def test_init(self):
        player = Player("fritz", "m")
        player.set_title("%s the great", includes_name_param=True)
        self.assertEqual("fritz", player.name)
        self.assertEqual("Fritz the great", player.title)
        self.assertEqual("", player.description)
        self.assertEqual("human", player.race)
        self.assertEqual("m", player.gender)
        self.assertEqual(set(), player.privileges)
        self.assertTrue(1 < player.stats["agi"] < 100)
    def test_tell(self):
        player = Player("fritz", "m")
        player.tell("line1")
        player.tell("line2")
        player.tell("ints", 42, 999)
        self.assertEquals("line1\nline2\nints 42 999\n", "".join(player.get_output_lines()))
        self.assertEquals([], player.get_output_lines())
    def test_look(self):
        player = Player("fritz", "m")
        attic = Location("Attic", "A dark attic.")
        self.assertEqual("[Limbo]\nThe intermediate or transitional place or state. Livings end up here if they're not inside a proper location yet.", player.look())
        player.move(attic)
        self.assertEqual("[Attic]", player.look(short=True))
        julie = NPC("julie", "f")
        julie.move(attic)
        self.assertEqual("[Attic]\nPresent: julie", player.look(short=True))


class TestDescriptions(unittest.TestCase):
    def test_name(self):
        item = Item("key")
        self.assertEquals("key", item.name)
        self.assertEquals("key", item.title)
        self.assertEquals("", item.description)
    def test_title(self):
        item = Item("key", "rusty old key")
        self.assertEquals("key", item.name)
        self.assertEquals("rusty old key", item.title)
        self.assertEquals("", item.description)
    def test_description(self):
        item = Item("key", "rusty old key", "a small old key that's rusted")
        self.assertEquals("key", item.name)
        self.assertEquals("rusty old key", item.title)
        self.assertEquals("a small old key that's rusted", item.description)
        item = Item("key", "rusty old key",
                    """
                    a very small, old key that's rusted
                    """)
        self.assertEquals("key", item.name)
        self.assertEquals("rusty old key", item.title)
        self.assertEquals("a very small, old key that's rusted", item.description)


if __name__ == '__main__':
    unittest.main()