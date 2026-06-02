from unittest.mock import MagicMock, patch

from chat4me.main import parse_args, print_window_list


def test_parse_args_defaults():
    args = parse_args([])
    assert args.config is None
    assert args.target_window is None
    assert args.llm_backend is None
    assert args.poll_interval is None
    assert args.log_level is None
    assert args.list_windows is False


def test_parse_args_all_flags():
    args = parse_args([
        "-c", "myconfig.yaml",
        "--target-window", "DiscordCanary",
        "--llm-backend", "openai",
        "--poll-interval", "3.5",
        "--log-level", "DEBUG",
        "--list-windows",
    ])
    assert args.config == "myconfig.yaml"
    assert args.target_window == "DiscordCanary"
    assert args.llm_backend == "openai"
    assert args.poll_interval == 3.5
    assert args.log_level == "DEBUG"
    assert args.list_windows is True


def test_parse_args_partial():
    args = parse_args(["--list-windows"])
    assert args.list_windows is True
    assert args.config is None


def test_parse_args_poll_interval_float():
    args = parse_args(["--poll-interval", "1.5"])
    assert args.poll_interval == 1.5


@patch("chat4me.screen.window.list_windows")
def test_print_window_list(mock_list):
    mock_list.return_value = ["Discord", "Code", "Browser"]
    print_window_list()
    mock_list.assert_called_once()
