# Joehnis_stoehnis
A small counter hosted in the local network to track Jönis stöhnis and the "seufzers" offers sounds and animations on clicking the counter.
# Seufz Counter

A tiny web counter ("Seufz counter") that lets you track "Jönis stöhnis".

Repository layout

- `src/app.py` - Flask web server (entrypoint).
- `src/counter.py` - Counter mechanics (thread-safe, file-persisted).
- `src/templates/index.html` - Minimal HTML+JS UI.
- `requirements.txt` - Python dependencies.
- `.gitignore`

- `app.py` — web server and routing (glue code).
- `counter.py` — counter logic, persistence.
- `templates/` and `static/` — HTML, CSS, JS UI assets.



How to install

Open PowerShell and run:

```powershell
git clone <>
cd Joehnis nis_sthönis
```

Install requirements when working with anaconda create new env

```powershell

pip install -r requirements.txt
```

Run locally

```powershell
cd Joehnis_stoehnis

python -m src.app
```

The server listens on port 5000 by default. Open `http://localhost:5000` in your browser.

Accessing from another device on your local network

1. Make sure the host machine allows incoming connections on port 5000 (check firewall).
2. Run the app bound to all interfaces (0.0.0.0). The example `app.py` in this repo already binds 0.0.0.0 when run directly.
3. Find the host machine IP (Windows PowerShell):

```powershell
ipconfig | Select-String "IPv4" -Context 0,0
```

4. From another device, open `http://<HOST_IP>:5000` (replace `<HOST_IP>` with the IPv4 address returned by ipconfig).

Notes and next steps

-  Production hosting, use a WSGI server (gunicorn, waitress) and configuring of TLS/reverse proxy.
