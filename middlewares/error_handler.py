from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
class error_handler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse :
        try:
            return await call_next(request)
        except Exception as e:

            response = {
                'message': 'Se presento un problema en la ejecucion del software, por favor recargue su programa he intente nuevamente',
                'type': 'error_handler',
                "error": str(e),
                "statud": False
            }
            return JSONResponse(status_code=500, content=response)