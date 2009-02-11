#   Copyright 2008, 2009 Aaron Barnes
#
#   This file is part of the FreeEMS project.
#
#   FreeEMS software is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   FreeEMS software is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with any FreeEMS software.  If not, see <http://www.gnu.org/licenses/>.
#
#   We ask that if you make any changes to this file you send them upstream to us at admin@diyefi.org

import comms.protocols as protocols, packet, __init__ as protocol


def getPacket(id):
    '''
    Return instance of requested protocol packet
    '''
    packetname = None
    
    # Check if we have a packet title for this id
    if id in protocol.RESPONSE_PACKET_TITLES:
        packetname = 'response'+protocol.RESPONSE_PACKET_TITLES[id]
    
    # Check if we have a class definition for this packet title
    if packetname and packetname in globals():
        return globals()[packetname]()
    else:
        return responseGeneric()


class response(packet.packet):
    '''
    Reponse packet
    '''

    _validation_rules = {}

    def __init__(self):
        '''
        Set defaults
        '''

        self._validation_rules = {
            'preset_payload_length': False,
            'requires_length': False,
        }


    def validate(self):
        '''
        Validate packet based on validation rules
        '''
        rules = self._validation_rules
        pid = self.getPayloadIdInt()

        if rules['preset_payload_length']:
            # Check payload is the required length
            if rules['preset_payload_length'] != self.getPayloadLengthInt():
                raise Exception, 'Packet type %d preset length of %s does not match the actual payload length of %s' % (pid, rules['preset_payload_length'], self.getPayloadLengthInt())
            
        if rules['requires_length']:
            # Check a length was supplied and the payload matches
            if not self.hasHeaderLengthFlag():
                raise Exception, 'Packet type %s was expecting a length flag to be set' % pid

            length = self.getPayloadLengthParsed()
            if not length:
                raise Exception, 'Packet type %s was expecting a length to be set' % pid

            if self.getPayloadLengthInt() != length:
                raise Exception, 'Packet type %s, payload length of %s does not match parsed length of %s' % (pid, self.getPayloadLengthInt(), length)


    def parsePayload(self, payload):
        '''
        Parse the payload
        '''
        if self.hasHeaderLengthFlag():
            # If length set, account for 2 length bytes
            self.setPayloadLengthParsed(payload[0:2])
            self.setPayload(payload[2:])

        else:
            self.setPayload(payload)


class responseGeneric(response):
    '''
    Generic EMS response for bad/not yet implemented packets
    '''

    def __init__(self):
        response.__init__(self)


class responseInterfaceVersion(response):
    '''
    EMS response to interface version request
    '''

    def __init__(self):
        response.__init__(self)
        rules = self._validation_rules
        rules['requires_length'] = True

    
    def createTestResponse(self, request):
        '''
        Run code to make an acurate test response
        '''
        self.setPayloadId(protocol.RESPONSE_INTERFACE_VERSION)
        self.setPayload('IFreeEMS_Vanilla001')


class responseFirmwareVersion(response):
    '''
    EMS response to firmware version request
    '''

    def __init__(self):
        response.__init__(self)
        rules = self._validation_rules
        rules['requires_length'] = True


    def createTestResponse(self, request):
        '''
        Run code to make an acurate test response
        '''
        self.setPayloadId(protocol.RESPONSE_FIRMWARE_VERSION)
        self.setPayload('FreeEMS_Vanilla_Test')


class responseMaxPacketSize(response):
    '''
    EMS response to max packet length request
    '''

    def __init__(self):
        response.__init__(self)
        rules = self._validation_rules
        rules['preset_payload_length'] = 2
    
    
    def createTestResponse(self, request):
        '''
        Run code to make an acurate test response
        '''
        self.setPayloadId(protocol.RESPONSE_MAX_PACKET_SIZE)
        self.setPayload([0, 255])


class responseEchoPacket(response):
    '''
    EMS response to echo packet request
    '''
    def __init__(self):
        response.__init__(self)
        rules = self._validation_rules
        rules['requires_length'] = 2


    def createTestResponse(self, request):
        '''
        Run code to make an acurate test response
        '''
        self.setPayloadId(protocol.RESPONSE_ECHO_PACKET_RETURN)
        self.setPayload(request.getPacketRawBytes())


class responseBasicDatalog(response):
    '''
    EMS basic datalog packet
    '''
    def __init__(self):
        response.__init__(self)
        rules = self._validation_rules
        rules['requires_length'] = True
