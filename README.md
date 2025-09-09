# Joehnis_stoehnis
A small counter hosted in the local network to track Jönis stöhnis and the "seufzers" offers sounds and animations on clicking the counter.
# Seufz Counter

A tiny web counter ("Seufz counter") that lets you track "Jönis stöhnis".

Repository layout

- `src/app.py` - Flask web server (entrypoint).
- `src/counter.py` - Counter mechanics (thread-safe, file-persisted).
- `src/templates/index.html` - Minimal HTML+JS UI.
- `requirements.txt` - Python dependencies.
- `templates/` and `static/` — HTML, CSS, JS UI assets.



How to install

Open PowerShell and run:

```powershell
git clone <https://github.com/Rich387/Joehnis_stoehnis.git>
```


Install requirements. When working with anaconda (miniconda) create new python env and install requirements.
When using minconda you can run all the commands in the anaconda comand prompt (execute with the specific enviroment)

```powershell

pip install -r requirements.txt
```

Run locally:
Navigate to the repository folder and run src.app (entry point)
 
```powershell
cd Joehnis_stoehnis

python -m src.app
```

The server listens on port 5000 by default. Open `http://localhost:5000` in your browser.

Accessing from another device on your local network

1. Make sure the host machine allows incoming connections on port 5000 (check firewall).
2. Find the host machine IP (Windows PowerShell):

```powershell
ipconfig | Select-String "IPv4" -Context 0,0
```

4. From another device, open `http://<HOST_IP>:5000` (replace `<HOST_IP>` with the IPv4 address returned by ipconfig).

Notes and next steps

-  Production hosting, use a WSGI server (gunicorn, waitress) and configuring of TLS/reverse proxy.
