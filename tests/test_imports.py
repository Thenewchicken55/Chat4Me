def test_import_main():
    from chat4me.main import main
    assert callable(main)
