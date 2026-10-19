# TRIBE LAB · BETA

Landing de TRIBE LAB con acceso a la beta de TribeBet (`/tribebet/`).

- Sitio estático (Render, `render.yaml`). Sin build: se publica la carpeta tal cual.
- **TribeBet beta = solo créditos de juego sin valor monetario.** Sin pagos, sin premios, sin retiros, puerta +18.
- Los originales viven en el vault de GoBig; `build.py` los copia y agrega la capa beta. Para actualizar: `python3 build.py && git commit -am "..." && git push` (Render redespliega solo).
