"""Flask app adapted from the original seufz_counter script.

This app keeps two counters (seufz, stoehn) with cooldowns, cookie-based
animation triggers and serves sound files from the `templates/` folder so
existing audio assets continue to work.
"""
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    make_response,
    request,
    send_from_directory,
)
from pathlib import Path
import time
import os
import argparse

import logging

base_dir = Path(__file__).parent
templates_dir = base_dir / "templates"
static_dir = base_dir / "static"
static_dir.mkdir(parents=True, exist_ok=True)

# Move audio files from templates -> static on first run so assets live in a
# proper place. This is best-effort and only moves files if they exist in
# templates and not already in static.
try:
    import shutil

    for fn in ("seufzer.mp3", "stöhner.mp3", "sad_sound.mp3"):
        srcf = templates_dir / fn
        dstf = static_dir / fn
        if srcf.exists() and not dstf.exists():
            shutil.move(str(srcf), str(dstf))
except Exception:
    # don't crash the app if file operations fail
    pass

# Configure Flask to serve from the new static folder
app = Flask(
    __name__,
    template_folder=str(templates_dir),
    static_folder=str(static_dir),
)
# new: simple logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
app.logger.setLevel(logging.INFO)
app.secret_key = os.environ.get("SEUFZ_SECRET", "seufz_secret")

data_dir = Path(__file__).parent.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)

seufz_store = data_dir / "seufz.json"
stoehn_store = data_dir / "stoehn.json"
from .counter import Counter

seufz = Counter(seufz_store)
stoehn = Counter(stoehn_store)

# timing state (kept in memory per-process)
last_seufz_time = 0
last_stoehn_time = 0
cooldown_seconds = 3

# HTML template is provided in src/templates/index.html — use render_template


def set_animation_cookie(response, value):
    # keep cookie alive slightly longer than cooldown so it survives until reload
    response.set_cookie("animation", value, max_age=(cooldown_seconds + 2), path="/", samesite="Lax")
    return response


@app.route("/", methods=["GET"])
def index():
    global last_seufz_time, last_stoehn_time
    now = time.time()
    seufz_disabled = (now - last_seufz_time) < cooldown_seconds
    stoehn_disabled = (now - last_stoehn_time) < cooldown_seconds
    return render_template(
        'index.html',
        seufz_count=seufz.get(),
        stoehn_count=stoehn.get(),
        seufz_disabled=seufz_disabled,
        stoehn_disabled=stoehn_disabled,
        cooldown_seconds=cooldown_seconds,
    )


@app.route("/seufz_increment", methods=["POST"])
def seufz_increment():
    global last_seufz_time
    if (time.time() - last_seufz_time) < cooldown_seconds:
        flash(f"Bitte warte {cooldown_seconds} Sekunden zwischen den Seufz-Klicks!")
        return redirect(url_for('index'))
    new = seufz.increment()
    last_seufz_time = time.time()
    resp = make_response(redirect(url_for('index')))
    return set_animation_cookie(resp, "seufz_plus")


@app.route("/seufz_decrement", methods=["POST"])
def seufz_decrement():
    global last_seufz_time
    if (time.time() - last_seufz_time) < cooldown_seconds:
        flash(f"Bitte warte {cooldown_seconds} Sekunden zwischen den Seufz-Klicks!")
        return redirect(url_for('index'))
    new = seufz.decrement()
    last_seufz_time = time.time()
    resp = make_response(redirect(url_for('index')))
    return set_animation_cookie(resp, "seufz_minus")


@app.route("/stoehn_increment", methods=["POST"])
def stoehn_increment():
    global last_stoehn_time
    if (time.time() - last_stoehn_time) < cooldown_seconds:
        flash(f"Bitte warte {cooldown_seconds} Sekunden zwischen den Stöhn-Klicks!")
        return redirect(url_for('index'))
    new = stoehn.increment()
    last_stoehn_time = time.time()
    resp = make_response(redirect(url_for('index')))
    return set_animation_cookie(resp, "stoehn_plus")


@app.route("/stoehn_decrement", methods=["POST"])
def stoehn_decrement():
    global last_stoehn_time
    if (time.time() - last_stoehn_time) < cooldown_seconds:
        flash(f"Bitte warte {cooldown_seconds} Sekunden zwischen den Stöhn-Klicks!")
        return redirect(url_for('index'))
    new = stoehn.decrement()
    last_stoehn_time = time.time()
    resp = make_response(redirect(url_for('index')))
    return set_animation_cookie(resp, "stoehn_minus")


@app.route('/sounds/<filename>')
def sounds(filename):
    static_dir = base_dir / 'static'
    return send_from_directory(str(static_dir), filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jönis Counter Web App")
    parser.add_argument("--set-seufz", type=int, help="Set the Seufz counter to a specific value and exit")
    parser.add_argument("--set-stoehn", type=int, help="Set the Stöhn counter to a specific value and exit")
    args = parser.parse_args()

    if args.set_seufz is not None:
        seufz.set(args.set_seufz)
        print(f"Seufz Counter set to {seufz.get()}.")
    elif args.set_stoehn is not None:
        stoehn.set(args.set_stoehn)
        print(f"Stöhn Counter set to {stoehn.get()}.")
    else:
        # single-process dev server avoids reloader state mismatch
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
