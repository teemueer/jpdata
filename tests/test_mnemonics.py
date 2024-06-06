def test_new_mnemonic_valid(default_user, fetch):
    soup, flash = fetch("/characters/一", data=dict(
        keyword="one",
        story="One line"
    ), flash=True)
    #print(soup.prettify())
    assert len(flash["msg"]) == 1
    assert len(flash["err"]) == 0
    assert soup.select_one("#keyword").get("value") == "one"
    assert soup.select_one("#story").text.strip() == "One line"