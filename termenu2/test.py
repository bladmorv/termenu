import sys
sys.path.append("..")
import unittest
import ansi
from termenu import Termenu

OPTIONS = ["%02d" % i for i in xrange(1,100)]
RESULTS = ["result-%02d" % i for i in xrange(1,100)]

def strmenu(menu):
    return menu._get_debug_view()

class Down(unittest.TestCase):
    def test_cursor_top(self):
        menu = Termenu(OPTIONS, height=3)
        assert strmenu(menu) == "(01) 02 03"
        menu._on_down()
        assert strmenu(menu) == "01 (02) 03"

    def test_cursor_middle(self):
        menu = Termenu(OPTIONS, height=3)
        menu.cursor = 1
        assert strmenu(menu) == "01 (02) 03"
        menu._on_down()
        assert strmenu(menu) == "01 02 (03)"

    def test_cursor_bottom(self):
        menu = Termenu(OPTIONS, height=3)
        menu.cursor = 2
        assert strmenu(menu) == "01 02 (03)"
        menu._on_down()
        assert strmenu(menu) == "02 03 (04)"

    def test_scroll_bottom_cursor_bottom(self):
        menu = Termenu(OPTIONS, height=3)
        menu.scroll = len(OPTIONS) - 3
        menu.cursor = 2
        assert strmenu(menu) == "97 98 (99)"
        menu._on_down()
        assert strmenu(menu) == "97 98 (99)"

class Up(unittest.TestCase):
    def test_cursor_top(self):
        menu = Termenu(OPTIONS, height=3)
        menu.cursor = 0
        assert strmenu(menu) == "(01) 02 03"
        menu._on_up()
        assert strmenu(menu) == "(01) 02 03"

    def test_cursor_middle(self):
        menu = Termenu(OPTIONS, height=3)
        menu.cursor = 1
        assert strmenu(menu) == "01 (02) 03"
        menu._on_up()
        assert strmenu(menu) == "(01) 02 03"

    def test_cursor_bottom(self):
        menu = Termenu(OPTIONS, height=3)
        menu.cursor = 2
        assert strmenu(menu) == "01 02 (03)"
        menu._on_up()
        assert strmenu(menu) == "01 (02) 03"

    def test_scroll_bottom_cursor_top(self):
        menu = Termenu(OPTIONS, height=3)
        menu.scroll = len(OPTIONS) - 3
        menu.cursor = 0
        assert strmenu(menu) == "(97) 98 99"
        menu._on_up()
        assert strmenu(menu) == "(96) 97 98"

class PageDown(unittest.TestCase):
    def test_cursor_top(self):
        menu = Termenu(OPTIONS, height=4)
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_pageDown()
        assert strmenu(menu) == "01 02 03 (04)"

    def test_cursor_middle(self):
        menu = Termenu(OPTIONS, height=4)
        menu.cursor = 1
        assert strmenu(menu) == "01 (02) 03 04"
        menu._on_pageDown()
        assert strmenu(menu) == "01 02 03 (04)"

    def test_cursor_bottom(self):
        menu = Termenu(OPTIONS, height=4)
        menu.cursor = 3
        assert strmenu(menu) == "01 02 03 (04)"
        menu._on_pageDown()
        assert strmenu(menu) == "05 06 07 (08)"

    def test_scroll_bottom_cursor_bottom(self):
        menu = Termenu(OPTIONS, height=4)
        menu.scroll = len(OPTIONS) - 4
        menu.cursor = 3
        assert strmenu(menu) == "96 97 98 (99)"
        menu._on_pageDown()
        assert strmenu(menu) == "96 97 98 (99)"

    def test_scroll_almost_bottom_cursor_bottom(self):
        menu = Termenu(OPTIONS, height=4)
        menu.scroll = len(OPTIONS) - 5
        menu.cursor = 3
        assert strmenu(menu) == "95 96 97 (98)"
        menu._on_pageDown()
        assert strmenu(menu) == "96 97 98 (99)"

class PageUp(unittest.TestCase):
    def test_cursor_top(self):
        menu = Termenu(OPTIONS, height=4)
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_pageUp()
        assert strmenu(menu) == "(01) 02 03 04"

    def test_cursor_middle(self):
        menu = Termenu(OPTIONS, height=4)
        menu.cursor = 2
        assert strmenu(menu) == "01 02 (03) 04"
        menu._on_pageUp()
        assert strmenu(menu) == "(01) 02 03 04"

    def test_cursor_bottom(self):
        menu = Termenu(OPTIONS, height=4)
        menu.cursor = 3
        assert strmenu(menu) == "01 02 03 (04)"
        menu._on_pageUp()
        assert strmenu(menu) == "(01) 02 03 04"

    def test_scroll_bottom_cursor_top(self):
        menu = Termenu(OPTIONS, height=4)
        menu.scroll = len(OPTIONS) - 4
        assert strmenu(menu) == "(96) 97 98 99"
        menu._on_pageUp()
        assert strmenu(menu) == "(92) 93 94 95"

    def test_scroll_almost_top_cursor_top(self):
        menu = Termenu(OPTIONS, height=4)
        menu.scroll = 1 
        assert strmenu(menu) == "(02) 03 04 05"
        menu._on_pageUp()
        assert strmenu(menu) == "(01) 02 03 04"

class Default(unittest.TestCase):
    def test_found(self):
        menu = Termenu(OPTIONS, height=4, default="03")
        assert strmenu(menu) == "01 02 (03) 04"

    def test_notfount(self):
        menu = Termenu(OPTIONS, height=4, default="asdf")
        assert strmenu(menu) == "(01) 02 03 04"

    def test_requires_scroll(self):
        menu = Termenu(OPTIONS, height=4, default="55")
        assert strmenu(menu) == "(55) 56 57 58"

    def test_last(self):
        menu = Termenu(OPTIONS, height=4, default="99")
        assert strmenu(menu) == "96 97 98 (99)"

    def test_before_last(self):
        menu = Termenu(OPTIONS, height=4, default="97")
        assert strmenu(menu) == "96 (97) 98 99"

    def test_multiple(self):
        menu = Termenu(OPTIONS, height=4, default=["05", "17", "93"])
        assert strmenu(menu) == "(05) 06 07 08"
        assert " ".join(menu.get_result()) == "05 17 93"

    def test_multiple_active(self):
        menu = Termenu(OPTIONS, height=4, default=["17", "05", "93"])
        assert strmenu(menu) == "(17) 18 19 20"
        assert " ".join(menu.get_result()) == "05 17 93"

    def test_multiple_empty_list(self):
        menu = Termenu(OPTIONS, height=4, default=[])
        assert strmenu(menu) == "(01) 02 03 04"
        assert " ".join(menu.get_result()) == "01"

class MultiSelect(unittest.TestCase):
    def test_select(self):
        menu = Termenu(OPTIONS, height=4)
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_space()
        menu._on_space()
        assert strmenu(menu) == "01 02 (03) 04"
        assert " ".join(menu.get_result()) == "01 02"
        assert " ".join(menu.get_result()) == "01 02"

    def test_deselect(self):
        menu = Termenu(OPTIONS, height=4)
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_space()
        assert " ".join(menu.get_result()) == "01"
        menu._on_up()
        menu._on_space()
        assert strmenu(menu) == "01 (02) 03 04"
        assert " ".join(menu.get_result()) == "02"

    def test_off(self):
        menu = Termenu(OPTIONS, height=4, multiselect=False)
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_space()
        assert strmenu(menu) == "(01) 02 03 04"
        assert " ".join(menu.get_result()) == "01"

class Results(unittest.TestCase):
    def test_single(self):
        menu = Termenu(OPTIONS, results=RESULTS, height=4)
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_down()
        menu._on_down()
        assert strmenu(menu) == "01 02 (03) 04"
        assert menu.get_result() == ["result-03"]

    def test_multiple(self):
        menu = Termenu(OPTIONS, results=RESULTS, height=4)
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_space()
        menu._on_space()
        assert strmenu(menu) == "01 02 (03) 04"
        assert menu.get_result() == ["result-01", "result-02"]

def active(s):
    return ansi.colorize(s, "black", "white")

def selected(s):
    return ansi.colorize(s, "red")

def active_selected(s):
    return ansi.colorize(s, "red", "white")

def white(s):
    return ansi.colorize(s, "white", bright=True)

class Decorate(unittest.TestCase):
    def test_active(self):
        menu = Termenu(OPTIONS, height=4)
        assert menu._decorate("text", active=True) == " " + active("text") + "  "

    def test_selected(self):
        menu = Termenu(OPTIONS, height=4)
        assert menu._decorate("text", selected=True) == "*" + selected("text") + "  "

    def test_active_selected(self):
        menu = Termenu(OPTIONS, height=4)
        assert menu._decorate("text", active=True, selected=True) == "*" + active_selected("text") + "  "

    def test_more_above(self):
        menu = Termenu(OPTIONS, height=4)
        assert menu._decorate("text", active=True, selected=True, moreAbove=True) == "*" + active_selected("text") + " " + white("^")

    def test_more_below(self):
        menu = Termenu(OPTIONS, height=4)
        assert menu._decorate("text", active=True, selected=True, moreBelow=True) == "*" + active_selected("text") + " " + white("v")

    def test_max_opti_on_len(self):
        menu = Termenu("one three fifteen twenty eleven".split(), height=4)
        assert menu._decorate("three", active=True, selected=True) == "*" + active_selected("three  ") + "  "

class DecorateFlags(unittest.TestCase):
    def test_active(self):
        menu = Termenu(OPTIONS, height=4)
        assert [menu._decorate_flags(i)["active"] for i in xrange(4)] == [True, False, False, False]

    def test_selected(self):
        menu = Termenu(OPTIONS, height=4)
        menu._on_down()
        menu._on_space()
        menu._on_space()
        assert [menu._decorate_flags(i)["selected"] for i in xrange(4)] == [False, True, True, False]

    def test_more_above_none(self):
        menu = Termenu(OPTIONS, height=4)
        assert [menu._decorate_flags(i)["moreAbove"] for i in xrange(4)] == [False, False, False, False]

    def test_more_above_one(self):
        menu = Termenu(OPTIONS, height=4)
        menu.scroll = 1
        assert [menu._decorate_flags(i)["moreAbove"] for i in xrange(4)] == [True, False, False, False]

    def test_more_below_one(self):
        menu = Termenu(OPTIONS, height=4)
        assert [menu._decorate_flags(i)["moreBelow"] for i in xrange(4)] == [False, False, False, True]

    def test_more_below_none(self):
        menu = Termenu(OPTIONS, height=4)
        menu.scroll = len(OPTIONS) - 4
        assert [menu._decorate_flags(i)["moreBelow"] for i in xrange(4)] == [False, False, False, False]

class Plugins(unittest.TestCase):
    def test_allow_default(self):
        class KeyLogger(object):
            def __init__(self):
                self.keys = []

            def _on_key(self, key):
                self.keys.append(key)
                return None # allow default code to run 

        plugin = KeyLogger()
        menu = Termenu(OPTIONS, height=4, plugins=[plugin])
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_key("down")
        assert strmenu(menu) == "01 (02) 03 04"
        assert plugin.keys == ["down"]

    def test_prevent_default(self):
        class OnlyKeyLogger(object):
            def __init__(self):
                self.keys = []

            def _on_key(self, key):
                self.keys.append(key)
                return True # prevent default code from running

        plugin = OnlyKeyLogger()
        menu = Termenu(OPTIONS, height=4, plugins=[plugin])
        assert strmenu(menu) == "(01) 02 03 04"
        menu._on_key("down")
        assert strmenu(menu) == "(01) 02 03 04"
        assert plugin.keys == ["down"]

if __name__ == "__main__":
    unittest.main()
