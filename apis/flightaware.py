#!/usr/bin/python

import sys
#from suds
# import suds
#
#from suds import null, WebFault
#from suds.client import Client
import logging
import flightaware_client
import requests
import base64
import utils

class FlightAware:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        self.base_url = "https://flightxml.flightaware.com/json/FlightXML2/"
        self.track = None

    def make_request(self, method, endpoint, params=None):
        r = None
        try:
            if method.upper() == "GET":
                r = requests.get("%s%s" % (self.base_url, endpoint), auth=(self.username, self.api_key), params=params)
                r.raise_for_status()
        except Exception as err:
            print(err)

        else:
            return r.json()

    def flight_search(self, ident):
        print("Searching FlightAware for %s" % ident)
        params = {"ident": ident}
        flights = self.make_request("get", "FlightInfo", params)
        if "FlightInfoResult" in flights:
            return flights['FlightInfoResult']['flights']

    def get_flight_id(self, ident, departTime):
        params = {"ident": ident, "departureTime": departTime}
        flight_id = self.make_request("get", "GetFlightID", params)
        if "GetFlightIDResult" in flight_id:
            return flight_id['GetFlightIDResult']
        else:
            return None

    def get_last_track(self, ident):
        params = {"ident": ident}
        track = self.make_request("get", "GetLastTrack", params)
        if "GetLastTrackResult" in track:
            return track['GetLastTrackResult']['data']

    def get_historical_flight_map(self, flightID):
        params = {"faFlightID": flightID, "mapHeight": 200, "mapWidth": 200}
        map_data = self.make_request("get", "MapFlightEx", params)
        if "MapFlightExResult" in map_data:
            img_data = map_data['MapFlightExResult']
            with open("%s.png" % flightID, "wb") as fh:
                fh.write(base64.b64decode(img_data))
            print("Saved to: %s.png" % flightID)

    def get_latest_flight_takeoff_time(self, ident):
        if self.track:
            track = self.track
        else:
            self.track = self.get_last_track(ident)
            track = self.track
        return track[0]['timestamp']

    def pretty_print_flight_info_short(self, flight):
        filed_depart = utils.format_liveatc_time(utils.convert_epoch(flight['filed_departuretime']))
        print("Ident: %s - Type: %s - Origin: %s - Destination: %s - Filed Depart Time: %s" % (flight['ident'], flight['aircrafttype'], flight['origin'], flight['destination'], filed_depart))