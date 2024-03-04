# YTshorts Generator

## creeds

- Pexels Api [Link]("https://www.pexels.com/api")
    ```conf
    [API]   
    api_key = apiKey without ""
    ```
- Google Api
    ```json
    {
        "web": {
            "client_id": "",
            "client_secret": "",
            "redirect_uris": [],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token"
        }
    }
    ```
    ### <p> If you donot know how to get these client_id client_secret then got to youtube and search for that there are planty of videos about this</p>

## Video Download

- #### If you want to download another video the  then got to the `main.py` change the below code
    ```python
    query = "cat"
    ```