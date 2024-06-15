![RetellAi](https://bookface-images.s3.amazonaws.com/logos/1a8537326cec1508a5051c913e288dcb0859143f.png)

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

## Structure for outbound call Api 

to_number - This is a text field where always has to be with the country code. Ex: +351 16516546815
custom_variables - this is an object

Examples: 
```bash
{
  "to_number":  "+3516969694",
  "custom_variables":
   {
    "name": "pepe"
   }
}
```

And then in your Retell Prompt you should add {{name}} 

## Webhook 

You can use Make (Formelly Integromat), Zapier  or anthoer webhook that you have. 

Configure de env variable called "MAKE_WEBHOOK_URL". 

## Call Status

You can access the twilio call status by using the `/call-status` which receives `call_sid` in the body 
```bash
{
  "call_sid": "iaosndoainwdoi"
}
```

Which is going to return an object with: 
```bash
{
  "sid": "asdasdasdasdsad",
  "duration": "4",
  "status": "completed",
  "direction": "outbound-api",
  "from": "+444444444",
  "to": "+444444444",
  "start_time": "2024-06-12T12:13:20+00:00",
  "end_time": "2024-06-12T12:13:24+00:00"
}
```





## Tutorial 

[Video](https://www.youtube.com/watch?v=Z5l54C3b6Ks) 


