from flask import request, make_response, redirect, url_for, flash, render_template
from app.customize import bp
from app.customize.forms import CustomizeForm


@bp.route("/toggle_theme")
def toggle_theme():
    cookies = request.cookies
    current_theme = cookies.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"

    next_page = request.args.get("next", url_for("main.index"))
    resp = make_response(redirect(next_page))
    resp.set_cookie("theme", new_theme)
    return resp


@bp.route("/customize", methods=["GET", "POST"])
def customize():
    form_data = {}
    for key, value in request.cookies.items():
        if value in ("true", "false"):
            value = True if value == "true" else False
        form_data[key] = value

    form = CustomizeForm(**form_data)
    if form.validate_on_submit():
        response = make_response(redirect(url_for("customize.customize")))
        response.set_cookie("theme", form.theme.data)
        response.set_cookie("nanori", str(form.nanori.data).lower())
        response.set_cookie("pinyin", str(form.pinyin.data).lower())
        response.set_cookie("krad", str(form.krad.data).lower())
        response.set_cookie("cjk", str(form.cjk.data).lower())
        response.set_cookie("variants", str(form.variants.data).lower())
        response.set_cookie("heisig", str(form.heisig.data).lower())
        response.set_cookie("halpern_kkd", str(form.halpern_kkd.data).lower())
        response.set_cookie("nelson_n", str(form.nelson_n.data).lower())
        response.set_cookie("jis", str(form.jis.data).lower())
        response.set_cookie("neighbors", form.neighbors.data)
        response.set_cookie("halpern_kkd_offset", str(form.halpern_kkd_offset.data))
        response.set_cookie("nelson_n_offset", str(form.nelson_n_offset.data))
        response.set_cookie("kanjikirja_offset", str(form.kanjikirja_offset.data))
        flash("Asetukset tallennettu", "success")
        return response

    return render_template("customize.html", form=form)
