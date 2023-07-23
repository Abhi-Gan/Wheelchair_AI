# Wheelchair_AI
chat server for questions about wheelchair

Run the server with the following command:
`python3 wheelchair_server.py`
The server should then run on http://127.0.0.1:5000. You'll be able to see this on the terminal.


ENDPOINTS:


**curbie_prompt**:
You can make POST requests to http://127.0.0.1:5000/curby_prompt which will be updated to respond to user prompts.
Your request should have a JSON body with field "query" mapping to a string query of the user prompt.

EX:

```
{
    "query": "how do i build a house?"
}
```


**top_reddit_posts**: GET request, optional param n default = 10
