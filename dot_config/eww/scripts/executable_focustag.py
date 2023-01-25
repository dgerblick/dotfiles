#!/usr/bin/env python

import dwm_ipc
import sys

if __name__ == '__main__':
    with dwm_ipc.IPCClient() as dwm_msg, dwm_ipc.IPCClient() as dwm_sub:
        dwm_msg.connect()
        monitor_num = int(sys.argv[1])
        tag_mask = int(sys.argv[2])
        monitors = dwm_msg.msg(dwm_msg.IPC_TYPE_GET_MONITORS)
        monitors = {x.get('num'): x for x in monitors}
        if not monitors.get(monitor_num).get('is_selected'):
            dwm_msg.msg(dwm_msg.IPC_TYPE_RUN_COMMAND, {
                        'command': 'focusmon', 'args': [monitor_num]})
        dwm_msg.msg(dwm_msg.IPC_TYPE_RUN_COMMAND, {
                    'command': 'view', 'args': [tag_mask]})
