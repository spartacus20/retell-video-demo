# retell-vide-demo

This is a sample demo repo to show how to have your own LLM plugged into Retell.

## Steps to run in localhost

1. First install dependencies

```bash
pip3 install -r requirements.txt
```

2. Fill out the API keys in `.env`

3. In another bash, use ngrok to expose this port to public network

```bash
ngrok http 8080
```

Note: If you have your server hosted just change NGROK_IP_ADDRESS for your domain ip address. For example https://yourdomain.com

4. Start the websocket server

```bash
python -m uvicorn server:app --reload --port=8080
```

You should see a fowarding address like
`https://dc14-2601-645-c57f-8670-9986-5662-2c9a-adbd.ngrok-free.app`, and you put on .env

## Tutorial 

[Video](https://www.youtube.com/watch?v=Z5l54C3b6Ks) 

