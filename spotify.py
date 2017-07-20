#
# Use the Spotify Web Connect API using credentials auth code and tokens.
#

import json
import requests
import time
import urlparse
import sys
from myopenhab import openhab
from myopenhab import mapValues
from myopenhab import getJSONValue


#   API Gateway
ACCOUNT_URL = 'https://accounts.spotify.com/api/token'
API_ROOT_URL = 'https://api.spotify.com/v1/me/player/'
REDIRECT_URI = 'http://openhabianpi.local:8080/static/spotify-auth.html'

class spotify(object):
    """

    A wrapper for the Spotify Web Connect API

    https://developer.spotify.com/web-api/web-api-connect-endpoint-reference/

    """
    def __init__(self):

        self.debug = False
        self.oh = openhab()

        self.client_id = self.oh.getState('spotify_client_id')
        self.client_secret = self.oh.getState('spotify_client_secret')

        self.access_token = self.oh.getState('spotify_access_token')
        self.refresh_token = self.oh.getState('spotify_refresh_token')
        self.token_issued = self.oh.getState('spotify_token_issued')
        self.token_expiry = self.oh.getState('spotify_token_expiry')

        if(self.token_expiry == "NULL"):
            self.refreshCredentials()
        if (self.access_token == "NULL"):
            self.generateCredentials()
        else:
            if (time.time() > float(self.token_expiry)):
                self.refreshCredentials()

    def generateCredentials(self):
        """
        Generate auth and refresh token for the very first time.
        """

        #   Send OAuth payload to get access_token
        payload = { 'code':self.oh.getState('spotify_auth_code'), 'client_id':self.client_id, 'client_secret':self.client_secret, 'redirect_uri':REDIRECT_URI, 'grant_type':'authorization_code' }

        print "-- Calling Token Service for the first time"

        try:
            r = requests.post(ACCOUNT_URL, data=payload, allow_redirects=False)

            if (self.debug): print r.headers
            if (self.debug): print r.json()
            resp = r.json()

            if(r.status_code == 200):
                access_token = resp['access_token']
                refresh_token = resp['refresh_token']
                expires_in = resp['expires_in']

                #   Set and Save the access token
                self.access_token = access_token
                self.refresh_token = refresh_token
                self.token_expiry = time.time() + float(expires_in)
                self.token_issued = time.strftime("%Y-%m-%dT%H:%M:%S")
                self.saveCredentials()
            else:
                print " -> Error getting token:" + str(resp)

        except:
            print " -> Error getting token:" + str(sys.exc_info()[1])

    def refreshCredentials(self):
        """
        If previous auth token expired, get a new one with refresh token.
        """

        #   Send OAuth payload to get access_token
        payload = { 'refresh_token':self.refresh_token, 'client_id':self.client_id, 'client_secret':self.client_secret, 'redirect_uri':REDIRECT_URI, 'grant_type':'refresh_token' }

        print "-- Calling Token Refresh Service"

        try:
            r = requests.post(ACCOUNT_URL, data=payload, allow_redirects=False)

            if (self.debug): print r.headers
            if (self.debug): print r.json()
            resp = r.json()

            if(r.status_code == 200):
                access_token = resp['access_token']
                expires_in = resp['expires_in']
                if('refresh_token' in resp):
                    refresh_token = resp['refresh_token']
                    self.refresh_token = refresh_token

                #   Set and Save the access token
                self.access_token = access_token
                self.token_expiry = time.time() + float(expires_in)
                self.token_issued = time.strftime("%Y-%m-%dT%H:%M:%S")
                self.saveCredentials()
            else:
                print " -> Error refreshing token:" + str(resp)

        except:
            print " -> Error refreshing token:" + str(sys.exc_info()[1])

    def saveCredentials(self):
        """
        Save current tokens to the openhab.
        """

        self.oh.sendCommand('spotify_access_token',self.access_token)
        self.oh.sendCommand('spotify_refresh_token',self.refresh_token)
        self.oh.sendCommand('spotify_token_expiry',self.token_expiry)
        self.oh.sendCommand('spotify_token_issued',self.token_issued)

    def call(self, path, mode=None, payload=None):
        """
        Call the API at the given path.
        """

        if (time.time() > self.token_expiry):
            self.refreshCredentials()
        headers = {"Authorization": "Bearer " + self.access_token, "Content-Type": "application/json" }
        if mode == "POST":
            r = requests.post(API_ROOT_URL + path,  headers=headers, data=payload)
            if(r.status_code != 202):
                print r.content
            return r.status_code
        elif mode == "PUT":
            r = requests.put(API_ROOT_URL + path,  headers=headers, data=payload)
            if(r.status_code != 202):
                print r.content
            return r.status_code
        else:
            r = requests.get(API_ROOT_URL + path,  headers=headers)
            if(r.status_code != 202):
                print r.content
            return r.json()

    def update(self):
        """
        Get a current player state.
        """
        print "-- Calling Service: Update"
        try:
            resp = self.call("")
            if (self.debug): print resp
            if ('item' in resp):

                self.oh.sendCommand('spotify_current_track', getJSONValue(resp, ['item','name']))
                self.oh.sendCommand('spotify_current_artist', getJSONValue(resp, ['item', 'artists', 0, 'name']))
                self.oh.sendCommand('spotify_current_cover', getJSONValue(resp, ['item', 'album', 'images', 1, 'url']))
                self.oh.sendCommand('spotify_current_duration', getJSONValue(resp, ['item', 'duration_ms']))
                self.oh.sendCommand('spotify_current_progress', getJSONValue(resp, ['progress_ms']))
                self.oh.sendCommand('spotify_current_progress', getJSONValue(resp, ['progress_ms']))
                self.oh.sendCommand('spotify_current_playing', mapValues(getJSONValue(resp, ['is_playing']), { 'True': 'ON', 'False': 'OFF' }))
                self.oh.sendCommand('spotify_current_device', getJSONValue(resp, ['device', 'name']))
                self.oh.sendCommand('spotify_current_volume', getJSONValue(resp, ['device', 'volume_percent']))
                self.oh.sendCommand('spotify_current_device_id', getJSONValue(resp, ['device', 'id']))

                print " -> Success"
            else:
                print " -> Item node missing from response :("
        except:
            print " -> Failure: ", sys.exc_info()[0]
            resp = ""

        return resp

    def volumeUp(self):
        """
        Volume up by 10%
        """
        print "-- Calling Service: Volume Up"
        try:
            vol = int(self.oh.getState('spotify_current_volume'))
            vol = int(round(vol/10)*10 + 10)
            if(vol>100):
                vol = 100
            print " -> Volume To:" + str(vol)
            resp = self.call("volume?volume_percent=" + str(vol),"PUT" )
            self.oh.sendCommand('spotify_current_volume',vol)
            if (self.debug): print resp
        except:
            print " -> VolumeUp Failure: ", sys.exc_info()[0]
            resp = ""

        return resp

    def volumeDown(self):
        """
        Volume down by 10%
        """
        print "-- Calling Service: Volume Down"
        try:
            vol = int(self.oh.getState('spotify_current_volume'))
            vol = int(round(vol/10)*10 - 10)
            if(vol<0):
                vol = 0
            print "Volume To:" + str(vol)
            resp = self.call("volume?volume_percent=" + str(vol),"PUT" )
            self.oh.sendCommand('spotify_current_volume',vol)
            if (self.debug): print resp
        except:
            print " -> VolumeDown Failure: ", sys.exc_info()[0]
            resp = ""

        return resp

    def pause(self):
        """
        Pause player
        """
        print "-- Calling Service: Pause"
        try:
            resp = self.call("pause","PUT")
            self.oh.sendCommand('spotify_current_playing',"OFF")
            if (self.debug): print resp
        except:
            print " -> Pause Failure: ", sys.exc_info()[0]
            resp = ""

        return resp

    def play(self, context_uri = None, new_device = None):
        """
        Resume player device
        """
        print "-- Calling Service: Play device"
        if (new_device is None):
            action_url = "play"
            print action_url
            if (context_uri is None):
                payload = {}
            else:
                payload = json.dumps({ 'context_uri': context_uri })
        else:
            if (context_uri is None):
                payload = json.dumps({ 'device_ids': [new_device] })
                action_url = ""
            else:
                payload = json.dumps({ 'context_uri': context_uri })
                action_url = "play?device_id=" + str(new_device)
        print payload
        print action_url

        try:
            resp = self.call(action_url,"PUT", payload = payload)
            if (self.debug): print resp
            self.update()
        except:
            print " -> Play Failure: ", sys.exc_info()[0]
            resp = ""

        return resp

    def previous(self):
        """
        Skip to previous track
        """
        print "-- Calling Service: Previous"
        try:
            resp = self.call("previous","POST")
            if (self.debug): print resp
            self.update()
        except:
            print " -> Previous Failure: ", sys.exc_info()[0]
            resp = ""

        return resp

    def next(self):
        """
        Skip to next track
        """
        print "-- Calling Service: Next"
        try:
            resp = self.call("next","POST")
            if (self.debug): print resp
            self.update()
        except:
            print " -> Next Failure: ", sys.exc_info()[0]
            resp = ""

        return resp


    def device_match(self, device_pick = None):
        """
        Identify device input type,(name, id or index).
        """
        print "-- Calling Service: devices_match"

        device_id_match=""
        index_test=""
        array_index=-1
#Dynamic check of id length against current id, with backup test if current id is null.

        try:
            if(device_pick):
                current_device_id = self.oh.getState('spotify_current_device_id')
                if( len(device_pick) == len(current_device_id) or len(device_pick) == 40):
                    array_index=1
                    print "id: ", device_pick
                else:
                    if (device_pick.isdigit() and len(device_pick) < 3):
                        array_index=2
                        print "index: ", device_pick
                    else:
                        print "name: ", device_pick
                        array_index=0

        except:
            print " -> Failure: ", sys.exc_info()[0]

        return array_index



    def devices(self, name = None, idNum = None, devIndex = None):
        """
        Get a current player devices and helper function to play device.
        """
        print "-- Calling Service: get devices"
        exitStatus=" -> Success"
        selected_device=""

        if (name) or (idNum) or (devIndex): exitStatus = ""
        if (devIndex) : iIndex = int(devIndex)
        else: iIndex = -1
        arrayDesc=[name,idNum,iIndex]
        try:
            resp = self.call("devices")
            if (self.debug): print resp
            if ('devices' in resp):
                self.oh.sendCommand('spotify_devices', json.dumps(resp))

                initOrder = 0
                partial = ""
                j = 0
                k = 1
                while(exitStatus == ""):
                    idx = 1
                    searchName = arrayDesc[(j%3)]
                    print "Match :", searchName , " or ", arrayDesc[((1 + j)%3)], "index: ", iIndex
                    intmed = str(searchName)
                    print intmed
                    print json.dumps(searchName)
                    for i in resp['devices']:
                        loopName = getJSONValue(i, ['name'])

                        searchid = getJSONValue(i, ['id'])
                        print idx, "Device : " , loopName , "id :" ,searchid
                        if (arrayDesc[(j%3)] ==  loopName) or (arrayDesc[((1 + j)%3)] == searchid) or (iIndex == idx ):
                            self.oh.sendCommand('spotify_device_name', loopName)
                            self.oh.sendCommand('spotify_device_id', searchid)
                            self.oh.sendCommand('spotify_device_index', idx)
                            exitStatus="Match Sucess"
                            selected_device = searchid
                            return selected_device
                        #Performs partial match serach if no results found
                        if (searchName):
                            if searchName.lower() in loopName.lower():
                                partial =  searchid
                        idx = idx + 1
                    #Looks at the various inputs and seraches on each input in various fields
                    iIndex=""
                    j+=1
                    if( j > 3): exitStatus="FAILED"
                    if (j == k):
                        k = 2
                        dev_desp=""
                        if (idNum):
                            dev_desp = idNum
                            idNum=""
                            j  = 0
                            initOrder = 1
                            print "idNum serach"
                        elif (devIndex) :
                            dev_desp = devIndex
                            devIndex=""
                            j  = 0
                            iIndex=-1
                            initOrder = 2
                            print "devinx serach"
                        elif (name) :
                            dev_desp = name
                            j  = 0
                            name = ""
                            initOrder = 0
                            print "name serach"
                        if (dev_desp):
                            smart_index = self.device_match(dev_desp)
                            if(smart_index > 0):
                                arrayDesc[smart_index] = dev_desp
                                if (smart_index == 2):
                                    iIndex = int(dev_desp)
                                if (smart_index == initOrder): j = j + 1

                        elif (partial):
                            k = 10
                            j = 3
                            arrayDesc[1] = partial
                            print "partial serach"

                print exitStatus
            else:
                print " -> Device list error :("
        except:
            print " -> Failure: ", sys.exc_info()[0]
            resp = ""
        return selected_device
    def removequotes(self,s): return "".join(i for i in s if i != "\"")
    def argsort(self, theargs = None):
        spotifyString="spotify:"
        myargs = ["",""]

        for i in range(2, len(theargs)):
            print theargs[i]
            stream=self.removequotes(theargs[i]).strip()
            if spotifyString in theargs[i].lower():
                myargs[0] = myargs[0]  + stream + " "
            else:
                myargs[1] = myargs[1] + stream + " "

        return self.removeEmpty(myargs)

    def removeEmpty(self, inString = None):
        print inString
        for i in range(len(inString)):
            if(inString[i] == ""):  inString[i] = None
            else: inString[i]=inString[i].strip()
        return inString


    def updateConnectionDateTime(self):
        self.oh.sendCommand('spotify_lastConnectionDateTime',time.strftime("%Y-%m-%dT%H:%M:%S+0000",time.gmtime(time.time())))

def main():

    t1 = time.time()

    c = spotify()

    args = sys.argv

    if(len(args) == 1):
        c.update()
    else:

        if(args[1] == "volume_up"):
            c.volumeUp()
        if(args[1] == "volume_down"):
            c.volumeDown()
        if(args[1] == "play"):
            if(len(args)>2):
                ma = c.argsort(args)
                c.play(ma[0],c.devices(ma[1]))
            else:
                c.play()
        if(args[1] == "pause"):
            c.pause()
        if(args[1] == "previous"):
            c.previous()
        if(args[1] == "next"):
            c.next()
        if(args[1] == "devices"):
            if(len(args)>2):
                ma = c.argsort(args)
                c.devices(ma[1])
            else:
                c.devices()
        if(args[1] == "device_id"):
            if(len(args)>2):
                c.devices(None,args[2])
            else:
                c.devices()
        if(args[1] == "device_name"):
            if(len(args)>2):
                ma = c.argsort(args)
                c.devices(ma[1])
            else:
                c.devices()
        if(args[1] == "device_index"):
            if(len(args)>2):
                c.devices(None, None, args[2])
            else:
                c.devices()
        if(args[1] == "play_device"):
            ma = c.argsort(args)
            c.play(ma[0], c.devices(ma[1]))
        if(args[1] == "play_device_name"):
            ma = c.argsort(args)
            c.play(ma[0], c.devices(ma[1]))


    c.updateConnectionDateTime()

    t2 = time.time()
    print "Done in " + str(t2-t1) + " seconds"

if __name__ == '__main__':
    main()
