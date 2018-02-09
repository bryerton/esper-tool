"""
ESPER Discovery Module
Used to send/receive/verify ESPER discovery packets
"""

import struct

class ESPERDiscovery(object):
    """ ESPER Discovery Object for requesting and getting discovery packets"""
    REVISION = 0
    IDENT_REQUEST_STR = "ESPER_DISCOVERY_REQUEST"
    IDENT_RESPONSE_STR = "ESPER_DISCOVERY_RESPONSE"

    def __init__(self, hardware_id="", device_type="", device_name="", module_id=0):
        """Initialize our discovery object, can skip if only using it for requests"""
        self.hardware_id = hardware_id
        self.device_type = device_type
        self.device_name = device_name
        self.module_id = module_id

    def verify_request(self, data=None):
        """Verify a packet is an ESPER REQUEST packet"""
        unpacked_data = struct.unpack_from("<B32s", data, 0)

        if unpacked_data[0] != self.REVISION:
            return False

        if unpacked_data[1].rstrip(' \t\r\n\0') != self.IDENT_REQUEST_STR:
            return False

        return True

    def verify_response(self, data=None):
        """Verify packet is an ESPER RESPONSE packet"""
        unpacked_data = struct.unpack_from("<B32s", data, 0)

        if unpacked_data[0] != self.REVISION:
            return False

        if unpacked_data[1].rstrip(' \t\r\n\0') != self.IDENT_RESPONSE_STR:
            return False

        return True

    def match_request(self, data):
        """Does this module match the criteria sent by the requestor"""
        if not self.verify_request(data):
            return False

        # Unpack full request
        unpacked_data = struct.unpack("<B32sB64sB64sB64sBI", data)

        # Check Hardware ID
        if unpacked_data[2] != 0:
            if unpacked_data[3].rstrip(' \t\r\n\0') != self.hardware_id:
                return False

        # Check Device Type
        if unpacked_data[4] != 0:
            if unpacked_data[5].rstrip(' \t\r\n\0') != self.device_type:
                return False

        # Check Device Name
        if unpacked_data[6] != 0:
            if unpacked_data[6].rstrip(' \t\r\n\0') != self.device_name:
                return False

        # Check Module ID
        if unpacked_data[8] != 0:
            if unpacked_data[9] != self.module_id:
                return False

        return True

    def get_response(self, data):
        """Receive Response, and parse it back into a python dict"""

        if not self.verify_response(data):
            return False

        unpacked_data = struct.unpack("<B32s64s64s64sI64s", data)

        response = dict()
        response['revision'] = unpacked_data[0]
        response['ident'] = unpacked_data[1].rstrip(' \t\r\n\0')
        response['hardware_id'] = unpacked_data[2].rstrip(' \t\r\n\0')
        response['device_type'] = unpacked_data[3].rstrip(' \t\r\n\0')
        response['device_name'] = unpacked_data[4].rstrip(' \t\r\n\0')
        response['module_id'] = unpacked_data[5]
        response['address'] = unpacked_data[6].rstrip(' \t\r\n\0')

        return response

    def send_response(self, address=""):
        """Send Response, should only be sent in response to discovery request match"""

        # Return response packet
        return struct.pack("<B32s64s64s64sI64s", \
            self.REVISION, \
            self.IDENT_RESPONSE_STR, \
            self.hardware_id, \
            self.device_type, \
            self.device_name, \
            self.module_id, \
            address)

    def send_request(self, hardware_id="", device_type="", device_name="", module_id=None):
        """Request a discovery packet from a given device(s) based on filter values given"""
        if hardware_id != "":
            use_hardware_id = 0xff
        else:
            use_hardware_id = 0x00

        if device_type != "":
            use_device_type = 0xff
        else:
            use_device_type = 0x00

        if device_name != "":
            use_device_name = 0xff
        else:
            use_device_name = 0x00

        if module_id != None:
            use_module_id = 0xff
        else:
            use_module_id = 0x00
            module_id = 0

        request_packet = struct.pack("<B32sB64sB64sB64sBI",  \
            self.REVISION, \
            self.IDENT_REQUEST_STR, \
            use_hardware_id, \
            hardware_id, \
            use_device_type, \
            device_type, \
            use_device_name, \
            device_name, \
            use_module_id, \
            module_id)

        return request_packet
