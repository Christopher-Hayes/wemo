from xml.dom import minidom
import requests

# request xml file and convert to xml object
def file_to_xml(xml_name='/setup.xml'):
    return minidom.parseString(request_file(xml_name))
# request file and return content
def request_file(file_name, print_headers=False):
    # Note: this is the usual URL when connected to WeMo device's network
    response = requests.get('http://10.22.22.1:49152' + file_name)
    if print_headers:
        print_headers(response)
    if str(response.status_code) != '200':
        print('Error: Request for ' + setup + ' failed.')
        exit(1)
    return response.content
# print headers from response object
def print_headers(response):
    print('Response Headers:')
    print('Status: ' + str(response.status_code))
    for key in response.headers.keys():
        print(key + ": " + response.headers[key])
    print('\n')
# get service xml objects
def get_services(root_xml):
    return root_xml.getElementsByTagName('serviceList')[0].getElementsByTagName('service')
# print + return services by name
def print_services(root_xml):
    print('Services:')
    lst = []
    for service in get_services(root_xml):
        s = service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue
        print(s)
        lst.append(s)
    return lst
# convenience method
def get_service_by_name(service_name, root_xml):
    for service in get_services(root_xml):
        if service_name.lower() == service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue:
            return service
    print('ERROR COULD NOT FIND CORRECT SERVICE')
# get actions by service xml, returns xml object
def get_actions(service_xml):
    return service_xml.getElementsByTagName('action')
# print + return service actions
def print_actions(service_xml):
    actions = get_actions(service_xml)
    lst = []
    for act in actions:
        s = act.getElementsByTagName('name')[0].firstChild.nodeValue
        print('    ' + s)
        lst.append(s)
    return lst
# convenience
def get_action_by_name(action_name, service_xml):
    for act in get_actions(service_xml):
        if action_name.lower() == act.getElementsByTagName('name')[0].firstChild.nodeValue:
            return act
    print("ERROR: COULD NOT FIND CORRECT ACTION")
# get action args by action xml; returns args as xml
def get_action_args(action_xml):
    return action_xml.getElementsByTagName('argumentList')[0].getElementsByTagName('argument')
# print + return action args
def print_action_args(action_xml):
    args = get_action_args(action_xml)
    lst = []
    for arg in args:
        s = arg.getElementsByTagName('name')[0].firstChild.nodeValue
        print('    ' + s)
        lst.append(s)
    return lst
# convenience
def get_action_arg_by_name(action_arg_name, action_xml):
    for arg in get_action_args(action_xml):
        if action_arg_name.lower() == arg.getElementsByTagName('name')[0].firstChild.nodeValue:
            return arg
    print("ERROR: COULD NOT FIND CORRECT ARG")
# assemble arguments + make request
def make_request(action_name, args=[], args_values=[], debug=False):
    # template
    pre =   '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>'
    post =  '</s:Body></s:Envelope>'
    # setup content
    pre +=  '<u:' + action_name + ' xmlns:u="urn:Belkin:service:basicevent:1">'
    post = '</u:' + action_name + '>' + post
    arg_str = ''
    for k,v in enumerate(args):
        name = v.getElementsByTagName('name')[0].firstChild.nodeValue
        arg_str += '<' + name + '>' + args_values[k] + '</' + name + '>'
    # assemble request
    content = pre + arg_str + post
    # make request
    response = requests.post('http://10.22.22.1:49152/upnp/control/basicevent1', data=content, headers={'Content-Type':'text/xml; charset="utf-8"', 'SOAPACTION':'"urn:Belkin:service:basicevent:1#' + action_name + '"'})
    print(response.status_code)
    print(response.content)
    # debug
    if debug:
        print_headers(response)
# eww
"""
def do_action(self, service_name, action_name):
    for act in self.get_service_actions(service_name):
        if action_name.lower() == act.getElementsByTagName('name')[0].firstChild.nodeValue.lower():
            caps_action_name = act.getElementsByTagName('name')[0].firstChild.nodeValue
            # print arguments
            act_args = act.getElementsByTagName('argumentList')[0].getElementsByTagName('argument')
            print('Optional Arguments:')
            for k, arg in enumerate(act_args):
                print('    ' + str(k) + ': ' + '[' + arg.getElementsByTagName('direction')[0].firstChild.nodeValue + ']\t' + arg.getElementsByTagName('name')[0].firstChild.nodeValue)
            print('Type the numbers of arguments you want to use separated by spaces.\nExample: 0 4 7 8')
            chosen_args_num = raw_input()
            chosen_args = []
            for k in chosen_args_num.split(' '):
                chosen_args.append(act_args[int(k)])
            # print chose
            print('Chosen Arguments:')
            for k in chosen_args:
                print('    ' + k.getElementsByTagName('name')[0].firstChild.nodeValue)
            print('If these arguments require setter input values then print the number followed by the desired input separated by a space.\nRepeat as needed. Type quit to move on to the next part.\nExample: 0 nutella\nExample: quit')
            for k, arg in enumerate(chosen_args):
                print('    ' + str(k) + ': ' + '[' + arg.getElementsByTagName('direction')[0].firstChild.nodeValue + ']\t' + arg.getElementsByTagName('name')[0].firstChild.nodeValue)
            input_args = ['' for k in range(len(chosen_args))]
            inpt = raw_input(': ')
            a1 = inpt.split(' ')[0]
            a2 = inpt[len(a1)+1:]
            while a1.lower() != 'quit':
                input_args[int(a1)] = a2
                inpt = raw_input(': ')
                a1 = inpt.split(' ')[0]
                a2 = inpt[len(a1)+1:]

            self.make_request(caps_action_name, arg_str, True)
"""
# sample
root_xml = file_to_xml()
service_xml = get_services(root_xml)
print_services(root_xml)
chosen_service = get_service_by_name('/eventservice.xml', root_xml)
print(chosen_service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue)
actions_xml = get_actions(chosen_service)
print_actions(chosen_service)
#chosen_action = get_action_by_name('changefriendlyname', chosen_service)
#actions_args = get_action_args(chosen_action)
#print_action_args(chosen_action)
