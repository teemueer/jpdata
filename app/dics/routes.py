from flask import abort, request, render_template
from app import db
from app.dics import bp
from app.dics.model import Dic


@bp.route("/dics/<string:name>/<int:idx>")
def dic_idx(name, idx):
    dics = (
        db.session.query(Dic)
        .where(Dic.name == name, idx >= Dic.idx_start, idx <= Dic.idx_end)
        .all()
    )

    if not dics:
        abort(404)

    if dics[-1].idx_end == idx:
        extra = (
            db.session.query(Dic)
            .where(Dic.name == name, Dic.page == dics[-1].page + 1)
            .scalar()
        )
        dics.append(extra)

    offset = request.cookies.get(f"{name}_offset", 0, type=int)

    page_from = dics[0].page + offset
    page_to = dics[-1].page + offset

    return render_template(
        "dic_idx.html", name=name, page_from=page_from, page_to=page_to
    )
