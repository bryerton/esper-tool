"""
ESPER Protocol
"""

# Added for python2 compat
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

import ipaddress
import random
import struct
import socket
import time

ESPER_API_VERSION = 2


class EsperHTTP:
    """Esper HTTP Protocol"""


class EsperUDP:
    """ESPER UDP Protocol"""

    ESPER_UDP_VERSION = 0

    __socket = None
    __auth_token = None

    def connect(self, ip, port, authToken):
        """Connect to an ESPER node (verify connection)"""
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((socket.INADDR_ANY, 0))
        self.__auth_token = authToken

    def send_discovery(self, deviceId, deviceName, deviceType, deviceRev, hardwareId, authToken, timeout=3, verbose=False):
        """Send a discovery packet and gather responses"""
        msg = self.__build_discovery_request(
            deviceId,
            deviceName,
            deviceType,
            deviceRev,
            hardwareId,
            authToken
        )
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.sendto(msg, ('<broadcast>', 27500))
        # Wait for response(s)
        timeout = timeout
        timeout_start = time.time()
        timeout_end = timeout_start + timeout
        response_list = []
        while time.time() < timeout_end:
            time_left = timeout_end - time.time()
            if(time_left <= 0):
                time_left = 0.01
            client.settimeout(time_left)
            try:
                data, server = client.recvfrom(1500)
                response = self.__parse_discovery_response(data[4:])
                if(response is not None):
                    response_list.append(response)
                    if(verbose):
                        print(response)
            except socket.timeout:
                # This is expected to occur, eventually all devices will have responded
                pass

        client.close()
        return response_list

    def __parse_discovery_response(self, data):
        """Receive Response, and parse it back into a python dict"""
        try:
            unpacked_data = struct.unpack("<BBI64s64s32s128sIxxxxxxxxxxxxIH64s", data)
            response = dict()
            response['api_version'] = unpacked_data[0]
            response['udp_version'] = unpacked_data[1]
            response['module_id'] = unpacked_data[2]
            response['name'] = unpacked_data[3].decode("ascii").rstrip(' \t\r\n\0')
            response['type'] = unpacked_data[4].decode("ascii").rstrip(' \t\r\n\0')
            response['revision'] = unpacked_data[5].decode("ascii").rstrip(' \t\r\n\0')
            response['hardware_id'] = unpacked_data[6].decode("ascii").rstrip(' \t\r\n\0')
            response['uptime'] = unpacked_data[7]
            response['ip'] = str(ipaddress.ip_address(unpacked_data[8]))
            response['port'] = unpacked_data[9]
            response['url'] = unpacked_data[10].decode("ascii").rstrip(' \t\r\n\0')
        except struct.error:
            response = None

        return response

    def __build_discovery_request(self, deviceId=None, deviceName="", deviceType="", deviceRev="", hardwareId="", authToken=""):
        """Build a discovery request packet to be sent, that looks for device(s) that match the given filter values"""
        if hardwareId != "":
            use_hardware_id = 0xff
        else:
            use_hardware_id = 0x00

        if deviceType != "":
            use_device_type = 0xff
        else:
            use_device_type = 0x00

        if deviceRev != "":
            use_device_rev = 0xff
        else:
            use_device_rev = 0x00

        if deviceName != "":
            use_device_name = 0xff
        else:
            use_device_name = 0x00

        if deviceId is not None:
            use_device_id = 0xff
            deviceId = int(deviceId)
        else:
            use_device_id = 0x00
            deviceId = int(0)

        # Build ESPER UDP request header
        request_header = struct.pack(
            "<4sBBBBI8s",
            "ESPR".encode("ascii"),  # ESPER Ident
            ESPER_API_VERSION,
            EsperUDP.ESPER_UDP_VERSION,
            0,  # CATEGORY (CAT_DISCOVERY)
            0,  # TYPE (DISCOVERY_REQUEST
            random.randint(0, 4294967295),  # MESSAGE ID
            authToken.encode("ascii")
        )

        request_payload = struct.pack(
            "<BBIB64sB64sB32sB128s",
            0,
            use_device_id,
            deviceId,
            use_device_type,
            deviceType.encode("ascii"),
            use_device_name,
            deviceName.encode("ascii"),
            use_device_rev,
            deviceRev.encode("ascii"),
            use_hardware_id,
            hardwareId.encode("ascii"))

        return request_header + request_payload
