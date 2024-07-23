import uvicorn
from server import app


#If you want to use the server for "reload" you should change "app" and put "server:app" and then add
#reload=True.
if __name__ == '__main__':
	uvicorn.run(app, host="0.0.0.0", port=80)

