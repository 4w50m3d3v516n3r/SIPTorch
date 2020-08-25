#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging, random
from core.requester import buildreq
from core.plugrun import runPlugin
from core.utils import parseMsg, catMetHead
from mutators.replparam import genRandStr

module_info = {
    'category'  :   'Application Layer Semantics',
    'test'      :   'OPTIONS With Unknown Proxy-Require and Require Scheme',
    'id'        :   'reqpreq'
}

def reqpreq():
    '''
    Require & Proxy-Require Implementation Stress

    This request tests proper implementation of SIP's Proxy-Require and
    Require extension mechanisms.

    Any element receiving this request will respond with a 420 Bad
    Extension response, containing an Unsupported header field listing
    these features from either the Require or Proxy-Require header field,
    depending on the role in which the element is responding.
    '''
    log = logging.getLogger('reqpreq')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseMsg(msg)
    # Tweak 1: Add Require & Proxy-Require fields
    head['Require'] = '%s, %s' % (genRandStr(10), random.getrandbits(32))
    head['Proxy-Require'] = '%s, %s' % (genRandStr(10), genRandStr(20))
    # Forming the request message back up
    mg = catMetHead(mline, head, body=body)
    return mg

def run(sock):
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(sock, reqpreq()):
        log.info('Module %s completed' % module_info['test'])
