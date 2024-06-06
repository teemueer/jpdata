def test_new_user_valid(fetch):
    soup, flash = fetch("/register", data=dict(
        username="teemu",
        email="teemu@email.com",
        password="salasana",
        password2="salasana"
    ), flash=True)
    assert len(flash["msg"]) == 1
    assert len(flash["err"]) == 0
    assert "Login" in soup.select_one("#navigation").text
    assert "Logout" not in soup.select_one("#navigation").text

    soup, flash = fetch("/login", data=dict(
        username="teemu",
        password="salasana",
    ), flash=True)
    assert len(flash["msg"]) == 1
    assert len(flash["err"]) == 0
    assert "Login" not in soup.select_one("#navigation").text
    assert "Logout" in soup.select_one("#navigation").text

    soup, flash = fetch("/logout", flash=True)
    assert len(flash["msg"]) == 1
    assert len(flash["err"]) == 0
    assert "Login" in soup.select_one("#navigation").text
    assert "Logout" not in soup.select_one("#navigation").text

    