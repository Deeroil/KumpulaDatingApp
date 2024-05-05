from flask import render_template

def tuplelist_helper(tuplelist):
    """make a list out of tuple list"""

    items = []
    for i in tuplelist:
        if i[0] not in items:
            items.append(i[0])

    if len(items) > 0:
        return items
    return None


def validate_register(username, passw, name, field, bio):
    if not username or not passw or not name or not field:
        return render_template("error.html", message="Missing information")

    if not 2 < len(username) < 26:
        return render_template(
            "error.html", message="Username should be 3-25 characters long"
        )

    if not 11 < len(passw) < 36:
        return render_template(
            "error.html", message="Password should be 12-35 characters long"
        )

    if not 1 < len(name) < 16:
        return render_template(
            "error.html", message="Name should be 2-15 characters long"
        )

    if not 2 < len(bio) < 200:
        return render_template(
            "error.html", message="Profile text should be 3-200 characters long"
        )

def validate_edit(name, bio):
    if not 1 < len(name) < 16:
        return render_template(
            "error.html", message="Name should be 2-15 characters long"
        )

    if not 2 < len(bio) < 200:
        return render_template(
            "error.html", message="Profile text should be 3-200 characters long"
        )
    
