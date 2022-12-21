#!/usr/bin/env python3

import dwm_ipc
import json


def css_classes(monitor_state, tag):
    class_names = ['selected', 'occupied', 'present']
    mask = tag.get('bit_mask')
    classes = [(x if (monitor_state.get(x) & mask) else None)
               for x in class_names]
    return ' '.join(filter(None, classes))


def print_state(state, tags):
    print(json.dumps({
        x: [
            {
                **tag,
                'css_classes': css_classes(state.get(x), tag)
            } for tag in tags
        ] for x in state
    }, separators=(',', ':')), flush=True)


def get_presence(dwm_msg: dwm_ipc.IPCClient, client_id):
    if client_id is None:
        return 0
    req = {'client_window_id': client_id}
    client = dwm_msg.msg(dwm_msg.IPC_TYPE_GET_DWM_CLIENT, req)
    return client.get('tags') or 0


if __name__ == '__main__':
    with dwm_ipc.IPCClient() as dwm_msg, dwm_ipc.IPCClient() as dwm_sub:
        dwm_msg.connect()
        dwm_sub.connect()
        tags = dwm_msg.msg(dwm_msg.IPC_TYPE_GET_TAGS)
        monitors = dwm_msg.msg(dwm_msg.IPC_TYPE_GET_MONITORS)

        # Get current monitor and initial tag state
        state = {}
        for monitor in monitors:
            monitor_num = monitor.get('num')
            tag_state = monitor.get('tag_state')
            client_id = monitor.get('clients', {}).get('selected')
            client = {}
            if client_id is not None:
                req = {'client_window_id': client_id}
                client = dwm_msg.msg(dwm_msg.IPC_TYPE_GET_DWM_CLIENT, req)
            state.update({monitor_num: {
                'client_id': client_id,
                'selected': tag_state.get('selected'),
                'occupied': tag_state.get('occupied'),
                'present': client.get('tags')
            }})

        dwm_sub.subscribe(dwm_sub.TAG_CHANGE_EVENT)
        dwm_sub.subscribe(dwm_sub.CLIENT_FOCUS_CHANGE_EVENT)

        while True:
            print_state(state, tags)
            event = dwm_sub.recv()

            # Process Event
            tag_change = event.get(dwm_sub.TAG_CHANGE_EVENT)
            if tag_change is not None:
                monitor_num = tag_change.get('monitor_number')
                new_state = tag_change.get('new_state')
                current_state = state.get(monitor_num)
                state.update({
                    monitor_num: {
                        **current_state,
                        'selected': new_state.get('selected'),
                        'occupied': new_state.get('occupied'),
                        'present': get_presence(dwm_msg, current_state.get('client_id'))
                    }
                })

            client_change = event.get(dwm_sub.CLIENT_FOCUS_CHANGE_EVENT)
            if client_change is not None:
                monitor_num = client_change.get('monitor_number')
                client_id = client_change.get('new_win_id')
                current_state = state.get(monitor_num)
                state.update({
                    monitor_num: {
                        **current_state,
                        'client_id': client_id,
                        'present': get_presence(dwm_msg, client_id),
                    }
                })
