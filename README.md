# FastMCP Server y Cliente

Servidor MCP ([server.py](./server.py)) y cliente ([client.py](./client.py)) construidos con [FastMCP](https://gofastmcp.com).

## Requisitos

* Python 3.10 o superior
* Acceso a internet (el cliente se conecta a un servidor MCP remoto)

## Instalación

Desde la raíz del repositorio, en PowerShell:

```powershell
# Crear el entorno virtual (solo la primera vez)
python -m venv .venv

# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación, ejecutar una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Configuración

Las variables se leen desde un archivo `.env` en la raíz (ver [config.py](./config.py)):

| Variable       | Descripción                                                                  |
| -------------- | ---------------------------------------------------------------------------- |
| `MCP_BASE_URL` | URL del servidor MCP. Por defecto `https://7680-fast-mcp-server.fastmcp.app/mcp` |
| `MCP_API_KEY`  | API key/token del servidor MCP, si requiere autenticación                    |

## Ejecutar el cliente

Con el entorno virtual activado:

```powershell
python client.py
```

Sin activarlo:

```powershell
.\.venv\Scripts\python.exe client.py
```

Salida esperada:

```text
Tools: ['greet', 'sum_two_numbers']
Resources: []
Prompts: []
Hello, Juan Perez!
```

> Usar `python` dentro del venv. El comando `python3` puede apuntar al Python global, donde `fastmcp` no está instalado (`ModuleNotFoundError: No module named 'fastmcp'`).

## Ejecutar el servidor localmente (opcional)

```powershell
python server.py
```

Para que el cliente use el servidor local, definir `MCP_BASE_URL` apuntando a él en `.env`.
