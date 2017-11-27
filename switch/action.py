from xml.dom import minidom
import requests

class action:
    def __init__(self, setup='deviceinfoservice.xml'):
        # get xml
        response = requests.get('http://10.22.22.1:49152/' + setup)
        if str(response.status_code) != '200':
            print('Error: Request for ' + setup + ' failed.')
            return
        # parse
        self.xml = minidom.parseString(response.content)
        self.actions = self.xml.getElementsByTagName('action')

    def get_actions(self):
        print('Actions:')
        for act in self.xml.getElementsByTagName('action'):
            print('    ' + act.getElementsByTagName('name')[0].firstChild.nodeValue)

    def do_action(self, action_name):
        for act in self.actions:
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
                inpt = raw_input()
                a1 = inpt.split(' ')[0]
                a2 = inpt[len(a1)+1:]
                while a1.lower() != 'quit':
                    input_args[int(a1)] = a2
                    inpt = raw_input()
                    a1 = inpt.split(' ')[0]
                    a2 = inpt[len(a1)+1:]
                arg_str = ''
                for k,v in enumerate(chosen_args):
                    name = v.getElementsByTagName('name')[0].firstChild.nodeValue
                    arg_str += '<' + name + '>' + input_args[k] + '</' + name + '>'
                self.make_request(caps_action_name, arg_str, True)

    def make_request(self, action_name, arg_str='', debug=False):
        # template
        pre =   '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>'
        post =  '</s:Body></s:Envelope>'
        # setup content
        pre +=  '<u:' + action_name + ' xmlns:u="urn:Belkin:service:basicevent:1">'
        post = '</u:' + action_name + '>' + post
        # assemble request
        content = pre + arg_str + post
        # make request
        response = requests.post('http://10.22.22.1:49152/upnp/control/basicevent1', data=content, headers={'Content-Type':'text/xml; charset="utf-8"', 'SOAPACTION':'"urn:Belkin:service:basicevent:1#' + action_name + '"'})
        print(response.status_code)
        print(response.content)
        # debug
        if debug:
            print('Status: ' + str(response.status_code))
            for key in response.headers.keys():
                print(key + ": " + response.headers[key])
            print('\n')

# sample
z = action('eventservice.xml')
z.get_actions()
z.do_action('ChangeFriendlyName')
z.do_action('GetFriendlyName')
