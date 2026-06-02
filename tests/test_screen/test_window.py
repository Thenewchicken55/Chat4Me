from unittest.mock import patch

from chat4me.screen.window import WindowInfo, find_window, list_windows


class MockWin:
    def __init__(
        self, title: str, visible: bool = True,
        width: int = 800, height: int = 600, left: int = 0, top: int = 0,
    ):
        self.title = title
        self.visible = visible
        self.width = width
        self.height = height
        self.left = left
        self.top = top


@patch("chat4me.screen.window.gw.getWindowsWithTitle")
def test_find_window_found(mock_get_wins):
    mock_get_wins.return_value = [MockWin("Discord - #general", visible=True, width=1200, height=800, left=100, top=50)]
    result = find_window("Discord")
    assert result is not None
    assert result.title == "Discord - #general"
    assert result.left == 100
    assert result.top == 50
    assert result.width == 1200
    assert result.height == 800


@patch("chat4me.screen.window.gw.getWindowsWithTitle")
def test_find_window_not_found(mock_get_wins):
    mock_get_wins.return_value = []
    result = find_window("Nonexistent")
    assert result is None


@patch("chat4me.screen.window.gw.getWindowsWithTitle")
def test_find_window_filters_invisible(mock_get_wins):
    mock_get_wins.return_value = [
        MockWin("Discord", visible=False, width=1200, height=800),
        MockWin("Discord", visible=True, width=1200, height=800),
    ]
    result = find_window("Discord")
    assert result is not None
    assert result.title == "Discord"


@patch("chat4me.screen.window.gw.getWindowsWithTitle")
def test_find_window_filters_zero_width(mock_get_wins):
    mock_get_wins.return_value = [
        MockWin("Discord", visible=True, width=0, height=0),
        MockWin("Discord", visible=True, width=1200, height=800),
    ]
    result = find_window("Discord")
    assert result is not None
    assert result.width == 1200


@patch("chat4me.screen.window.gw.getAllWindows")
def test_list_windows(mock_get_all):
    mock_get_all.return_value = [
        MockWin("Discord - #general"),
        MockWin("", visible=True),
        MockWin("Code"),
        MockWin("Discord - #general"),
    ]
    titles = list_windows()
    assert "Discord - #general" in titles
    assert "Code" in titles
    assert "" not in titles
    assert len(titles) == 2


def test_window_info_named_tuple():
    wi = WindowInfo(title="Test", left=10, top=20, width=100, height=200)
    assert wi.title == "Test"
    assert wi.left == 10
    assert wi.top == 20
    assert wi.width == 100
    assert wi.height == 200
    _, _, right, bottom = wi.left, wi.top, wi.left + wi.width, wi.top + wi.height
    assert right == 110
    assert bottom == 220
