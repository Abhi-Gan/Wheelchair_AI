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

Example response (string):

" A good wheelchair for trails outdoors is one that is designed for off-road use. Look for wheelchairs with large, knobby tires, a low center of gravity, and a suspension system to help absorb bumps and shocks. You may also want to consider a wheelchair with adjustable seat height and backrest angle, as well as adjustable armrests and footrests."

**top_reddit_posts**: GET request, optional param n default = 10

http://127.0.0.1:5000/top_reddit_posts

Results are a list of dictionaries {"submission":"<reddit post title>", "url":"link to post"}
