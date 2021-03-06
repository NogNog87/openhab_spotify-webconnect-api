# openhab_spotify-webconnect-api
A simple Python script to integrate Spotify's Web Connect API (https://developer.spotify.com/web-api/web-api-connect-endpoint-reference/) to OpenHab (openhab.org)

I've just found the amazing work by pmpkk and added some features around devices, giving you full control and allowing you to easily use Alexa and Home devices to control spotify on different devices with IFFT setups. They should be backporting all the good stuff so use his version
pmpkk/openhab_spotify-webconnect-api

You can do stuff like 
python spotify.py play spotify:album:4DEZVbAxlZPRXWCHUV5wF3 “Jem’s Echo”
or 
python spotify.py play Jem


<h1>Prerequisite</h1>

* OpenHab 2.1 installed on Raspberry Pi (or similar)
* OpenHab REST installed
* Spotify User Account
* Spotify Developer Account
* Know your OpenHab root URL/IP and port. In this doc, I assume http://openhabianpi.local:8080/

<h1>Instructions</h1>

1. Add the spotify.items file into openhab-conf/items and verify they have been added to your setup in Paper UI

* Check by asking the rest API: http://openhabianpi.local:8080/rest/items/spotify_auth_code
* You should get a successful JSON response

2. Place the following files in the folders:

* matrix-theme.css into openhab-conf/html/matrix-theme
* AppIcons.svg into openhab-conf/html/matrix-theme
* spotify-auth.html into openhab-conf/html
* myopenhab.py into openhab-conf/scripts
* spotify.py into openhab-conf/scripts
* spotify.rules into openhab-conf/rules
* spotify.items into openhab-conf/items

3. Verify you can reach spotify-auth.html

* Go to: http://openhabianpi.local:8080/static/spotify-auth.html
* You should see a page called "Spotify Integration" with a status message "spotify_client_id" missing

4. After registering as a Spotify developer, create a new App and retrieve client id and secret:

* Goto https://developer.spotify.com/my-applications/#!/applications
* Click "Create App"
* Provide a name and description
* Set the Redirect URI to:  http://openhabianpi.local:8080/static/spotify-auth.html
* Save the Settings

5. Give the client id and secret to OpenHab

* Save the Client ID to spotify_client_id in OpenHab (e.g. through openhab CLI smarthome:update spotify_client_id {your_id})
* Copy the Client Secret to spotify_client_secret in OpenHab (e.g. through the rest API)

6. Authenticate your New App for your Spotify User

* Go to: http://openhabianpi.local:8080/static/spotify-auth.html
* You should see a page called "Spotify Integration" with a status message "Click here to Authenticate"
* Click the link and authenticate your app
* When done, the page returns and displays "New Auth Code successfully saved to OpenHab!"
* Check that the spotify_auth_code is set in OpenHab

7. Test spotify.py in SSH

* Set the REDIRECT_URI in spotify.py to the right value
* Run this in terminal /usr/bin/python /etc/openhab2/scripts/spotify.py

You should see this:

```python
Successfully got state from OpenHab: spotify_client_id
Successfully got state from OpenHab: spotify_client_secret
Successfully got state from OpenHab: spotify_access_token
Successfully got state from OpenHab: spotify_refresh_token
Successfully got state from OpenHab: spotify_token_issued
Successfully got state from OpenHab: spotify_token_expiry
-- Calling Service: Update
Successfully posted state to OpenHab: spotify_current_track
Successfully posted state to OpenHab: spotify_current_artist
Successfully posted state to OpenHab: spotify_current_cover
Successfully posted state to OpenHab: spotify_current_duration
Successfully posted state to OpenHab: spotify_current_progress
Successfully posted state to OpenHab: spotify_current_progress
Successfully posted state to OpenHab: spotify_current_playing
Successfully posted state to OpenHab: spotify_current_device
Error posting state to OpenHab: spotify_current_volume (HTTP Response 400)
Successfully posted state to OpenHab: spotify_current_device_id
 -> Success
Successfully posted state to OpenHab: spotify_lastConnectionDateTime
Done in 0.761183977127 seconds
```

8. You can now hook up OpenHab rules or HabPanel with the data in the spotify items.

<h1>Use</h1>

* spotify.py
* parameters:
  * none = refresh data
  * play = resume playing
  * play uri = play suported uris (album, artist or playlist), e.g. spotify:user:spotify:playlist:37i9dQZF1DX5OepaGriAIm
  * pause = pause
  * next = next track
  * previous = previous track
  * volume_up = 10% up
  * volume_down = 10% down
