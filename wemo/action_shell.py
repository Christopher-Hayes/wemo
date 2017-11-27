import action

verbose = False

action = action.action()
root_xml = action.file_to_xml()
# Service loop
while True:
    print('\nSERVICE LIST')
    if verbose:
        print('Pick a service to get available actions.\nSelect by typing in the given integer. Example: 3\nType quit to exit.')
    else:
        print('Commands: <service_int>, back, quit')
    action.print_services(root_xml, True)
    inpt = raw_input(': ')
    if inpt.lower() == 'quit':
        exit(0)
    service = action.get_services(root_xml)[int(inpt)]    # xml snippet in setup.xml
    service_name = service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue
    service_xml = action.get_service_file(service)        # full xml file associated to snippet 'service'
    # Action loop
    action_loop = True
    while action_loop:
        print('\nACTION LIST\t(Service: ' + service_name + ')')
        if verbose:
            print('Pick an action to see action arguments.\nSelect by typing in the given integer. Example: 3\nType back to return to Service view.\nType quit to exit.')
        else:
            print('Commands: <action_integer>, back, quit')
        action.print_actions(service_xml, True)
        inpt = raw_input(': ')
        if inpt.lower() == 'quit':
            exit(0)
        elif inpt.lower() == 'back':
            break
        action_xml = action.get_actions(service_xml)[int(inpt)]
        action_name = action_xml.getElementsByTagName('name')[0].firstChild.nodeValue
        # Action Arguments loop
        arg_loop = True
        while arg_loop:
            total_args = action.get_action_args(action_xml)
            if len(total_args) > 0:
                print('\nACTION ARGUMENT LIST\t(Action: ' + action_name + ')')
                if verbose:
                    print('Choose the arguments to make custom inputs for.\nSelect by typing in the given integer(s) separated by a space.\nSetting input for an [out] argument will have no effect.\nExample: 2 6 4 9\nType back to return to Action view.\nType quit to exit.')
                else:
                    print('Commands: <arg_integer>, back, quit\t\t*ignore [out]')
                action.print_action_args(action_xml, True)
                inpt = raw_input(': ')
                if inpt.lower() == 'quit':
                    exit(0)
                elif inpt.lower() == 'back':
                    break
                chosen_args = [] if len(inpt) == 0 else list(map(lambda k: total_args[int(k)], inpt.split(' ')))
                # set inputs
                print('\nARGUMENT INPUTS')
                if verbose:
                    print('This program will now loop through the arguments to allow you\nto set a specific input for the argument.\nSetters: Type the input and hit enter.\nGetters: Hit enter to skip.\nType quit to exit')
                else:
                    print('Commands: (Setters:) <custom_input>, (Getters:) <>, back, quit')
                args_inpts = ['' for k in range(len(chosen_args))]
                for k,arg in enumerate(chosen_args):
                    inpt = raw_input('    ' + arg.getElementsByTagName('name')[0].firstChild.nodeValue + ': ')
                    if inpt.lower() == 'quit':
                        exit(0)
                    args_inpts[k] = inpt
            else:
                chosen_args = args_inpts = []
            # review settings
            print('\nCURRENT SETTINGS:')
            print('    Service: ' + service_name)
            print('    Action: ' + action_name)
            if len(total_args) > 0:
                print('    Action Arguments:')
                for k,arg in enumerate(chosen_args):
                    print('        ' + arg.getElementsByTagName('name')[0].firstChild.nodeValue + ' : ' + args_inpts[k])
            inpt = raw_input('\nReady to run action with these settings? (Y/N): ')
            if 'y' in inpt.lower():
                # chosen arguments list is converted from xml (minidom) objects to the name attribute
                action.make_request(service, action_name, chosen_args, args_inpts)
                action_loop = arg_loop = False
            else:
                if len(total_args) == 0:
                    print('Returning to action loop...')
                    break
                else:
                    print('Returning to action arguments loop...')
                    pass
