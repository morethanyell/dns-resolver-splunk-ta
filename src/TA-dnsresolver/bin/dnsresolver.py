#!/usr/bin/env python

import sys
import socket
import re
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators


@Configuration()
class dnsresolver(StreamingCommand):

    inpf = Option(
        doc='''
        **Syntax:** **input=***<input_field_name>*
        **Description:** Name of the field containing URL or domain name string.''',
        require=True, validate=validators.Fieldname())

    outf = Option(
        doc='''
        **Syntax:** **output=***<output_field_name>*
        **Description:** Customize the name of the field that will contain the resolved IPv4 address.''',
        require=False, default="ipv4_addr")

    outfipv6 = Option(
        doc='''
        **Syntax:** **output=***<output_field_name>*
        **Description:** Customize the name of the field that will contain the resolved IPv6 address.''',
        require=False, default="ipv6_addr")

    port = Option(
        doc='''
        **Syntax:** **port=***80*
        **Description:** Speficy the port to use in calling the `getaddrinfo` function.''',
        require=False, default="80")

    verbose = Option(
        doc='''
        **Syntax:** **verbose=***<true|false>*
        **Description:** Set to true to generate more fields such as `ipv6_addr`, `fqdn`, and `addr_info`''',
        require=False, default=False, validate=validators.Boolean())

    def stream(self, events):

        if self.outf.__eq__(self.outfipv6): raise Exception("Field names for output of IPv4 and IPv6 address must not be the same.")

        for event in events:

            resolved = self.resolver(event[self.inpf], self.port)

            addrinfo = resolved[1]

            if addrinfo is not None:
                ipv4 = 'n/a' if len(addrinfo) < 1 else addrinfo[0][4][0]
                ipv6 = 'n/a' if len(addrinfo) < 4 else addrinfo[4][4][0]

                if addrinfo is not None:
                    if not self.verbose:
                        event[self.outf] = ipv4
                    else:
                        event[self.outf] = ipv4
                        event[self.outfipv6] = ipv6
                        event['treated_url'] = resolved[0]
                        event['fqdn'] = socket.getfqdn(ipv4)
                        event['full_socket_detail'] = addrinfo

            yield event

    @staticmethod
    def resolver(url, port=80):

        url_treated = re.findall('^(?:https?\:\/\/)?([^\:\/]+)[\:\/]?', url)

        url_treated = url_treated[0] if url_treated else ""

        try:
            addrinfo = socket.getaddrinfo(url_treated, port)
        except:
            addrinfo = None

        return (url_treated, addrinfo)


dispatch(dnsresolver, sys.argv, sys.stdin, sys.stdout, __name__)
