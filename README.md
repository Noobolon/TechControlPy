# TechControlPy

## Setup:

* Criar ambiente virtual:<br> 
    Windows:
    ```sh
    python -m venv .venv
    venv\Scripts\activate.bat
    ```

    Linux / MacOS:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

---

* Instalar dependências:
```sh
pip install -r requirements.txt
```

---

* Rodar API:
```sh
fastapi dev main.py
```