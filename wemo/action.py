from xml.dom import minidom
import requests

class action:
    # request xml file and convert to xml object
    def file_to_xml(self, xml_name='/setup.xml', print_headers_arg=False):
        return minidom.parseString(self.request_file(xml_name, print_headers_arg))
    # request file and return content
    def request_file(self, file_name, print_headers_arg=False):
        # Note: this is the usual URL when connected to WeMo device's network
        response = requests.get('http://10.22.22.1:49152' + file_name)
        if print_headers_arg:
            self.print_headers(response)
        if str(response.status_code) != '200':
            print('Error: Request for ' + setup + ' failed.')
            exit(1)
        return response.content
    # print headers from response object
    def print_headers(self, response):
        print('Response Headers:')
        print('Status: ' + str(response.status_code))
        for key in response.headers.keys():
            print(key + ": " + response.headers[key])
        print('\n')
    # get service xml objects
    def get_services(self, root_xml):
        return root_xml.getElementsByTagName('serviceList')[0].getElementsByTagName('service')
    # print + return services by name
    def print_services(self, root_xml, numbered=False):
        lst = []
        print('Services:')
        for k,service in enumerate(self.get_services(root_xml)):
            s = service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue
            print('    ' + ((str(k) + ': ') if numbered else '') + s)
            lst.append(s)
        return lst
    # convenience method
    def get_service_by_name(self, service_name, root_xml):
        for service in self.get_services(root_xml):
            if service_name.lower() == service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue.lower():
                return service
        print('ERROR COULD NOT FIND CORRECT SERVICE')
    # use service xml snippet from setup.xml to get related xml file
    def get_service_file(self, service_xml):
        return self.file_to_xml(service_xml.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue)
    # get actions by service xml, returns xml object
    def get_actions(self, service_xml):
        return service_xml.getElementsByTagName('action')
    # print + return service actions
    def print_actions(self, service_xml, numbered=False):
        actions = self.get_actions(service_xml)
        lst = []
        print('Actions:')
        for k,act in enumerate(actions):
            s = act.getElementsByTagName('name')[0].firstChild.nodeValue
            print('    ' + ((str(k) + ': ') if numbered else '') + s)
            lst.append(s)
        return lst
    # convenience
    def get_action_by_name(self, action_name, service_xml):
        for act in self.get_actions(service_xml):
            if action_name.lower() == act.getElementsByTagName('name')[0].firstChild.nodeValue.lower():
                return act
        print("ERROR: COULD NOT FIND CORRECT ACTION")
    # get action args by action xml; returns args as xml
    def get_action_args(self, action_xml):
        try:
            return action_xml.getElementsByTagName('argumentList')[0].getElementsByTagName('argument')
        except IndexError:
            # action does not have any arguments
            return []
    # print + return action args
    def print_action_args(self, action_xml, numbered=False):
        args = self.get_action_args(action_xml)
        # check that action has arguments
        if len(args) == 0:
            return []
        lst = []
        print('Action Arguments:')
        for k,arg in enumerate(args):
            s = arg.getElementsByTagName('name')[0].firstChild.nodeValue
            d = arg.getElementsByTagName('direction')[0].firstChild.nodeValue
            print('    ' + ((str(k) + ': ') if numbered else '') + '[' + d + ']\t' + s)
            lst.append(s)
        return lst
    # convenience
    def get_action_arg_by_name(self, action_arg_name, action_xml):
        for arg in self.get_action_args(action_xml):
            if action_arg_name.lower() == arg.getElementsByTagName('name')[0].firstChild.nodeValue.lower():
                return arg
        print("ERROR: COULD NOT FIND CORRECT ARG")
    # assemble arguments + make request
    def make_request(self, service_xml, action_name, args_names=[], args_values=[], debug=False):
        # template
        pre =   '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>'
        post =  '</s:Body></s:Envelope>'
        # setup content
        pre +=  '<u:' + action_name + ' xmlns:u="' + service_xml.getElementsByTagName('serviceType')[0].firstChild.nodeValue + '">'
        post = '</u:' + action_name + '>' + post
        arg_str = ''
        for k,v in enumerate(args_names):
            # don't include in content if empty (getter arguments will not appear in request, but show up as arguments regardless)
            if len(args_values[k]) > 0:
                name = v.getElementsByTagName('name')[0].firstChild.nodeValue
                arg_str += '<' + name + '>' + args_values[k] + '</' + name + '>'
        # assemble request
        content = pre + arg_str + post
        # make request
        response = requests.post('http://10.22.22.1:49152' + service_xml.getElementsByTagName('controlURL')[0].firstChild.nodeValue, data=content, headers={'Content-Type':'text/xml; charset="utf-8"', 'SOAPACTION':'"' + service_xml.getElementsByTagName('serviceType')[0].firstChild.nodeValue + '#' + action_name + '"'})
        #print(content + '\n- - - - - - -')
        #print(response.content)
        # response
        if not 'UPnPError' in response.content:
            print('\nOperation successful!\nResponse:\n')
            self.parse_response(response.content)
        else:
            print('ERROR: Response:\n' + response.content)
        # debug
        if debug:
            print(response.content)
        # debug
        if debug:
            self.print_headers(response)
    # parse response
    def parse_response(self, response):
        try:
            data_start = response.index('>', response.index('<u:')) + 3
            data_end   = response.index('</u:') - 2
            data       = '<root>' + self.remove_shells(response[data_start:data_end]) + '</root>' # Note: xml must have root element
            data_xml   = minidom.parseString(data)
            for arg in data_xml.getElementsByTagName('root')[0].childNodes:
                if arg.nodeName != '#text':
                    print(arg.nodeName + ':\t' + ('\t' if len(arg.nodeName) < 15 else '') + arg.firstChild.nodeValue)
        except Exception as e:
            # no arguments returned or malformed xml
            print('Warning: ' + e.message)
            return
    # recursively remove outer elements
    def remove_shells(self, data):
        # replace encoding weirdness
        data = data.replace('&lt;', '<').replace('&gt;', '>')
        # check there is more than one set of tags, if not just return
        if data.count('</') < 2:
            return data
        # parse outer tag
        s1 = data.index('<')
        s2 = data.index('>')
        tag = data[s1+1:s2]
        end_tag = data.index('</' + tag + '>')
        # check if it is the last tag
        if end_tag == len(data) - 3 - len(tag):
            # return inner content only
            return self.remove_shells(data[s2 + 1:end_tag])
        else:
            return data
