import socket
import json
import struct


class IPCClient(socket.socket):
    IPC_TYPE_RUN_COMMAND = 0
    IPC_TYPE_GET_MONITORS = 1
    IPC_TYPE_GET_TAGS = 2
    IPC_TYPE_GET_LAYOUTS = 3
    IPC_TYPE_GET_DWM_CLIENT = 4
    IPC_TYPE_SUBSCRIBE = 5
    IPC_TYPE_EVENT = 6

    TAG_CHANGE_EVENT = 'tag_change_event'
    LAYOUT_CHANGE_EVENT = 'layout_change_event'
    CLIENT_FOCUS_CHANGE_EVENT = 'client_focus_change_event'
    MONITOR_FOCUS_CHANGE_EVENT = 'monitor_focus_change_event'
    FOCUSED_TITLE_CHANGE_EVENT = 'focused_title_change_event'
    FOCUSED_STATE_CHANGE_EVENT = 'focused_state_change_event'

    def __init__(self) -> None:
        super().__init__(socket.AF_UNIX)

    def connect(self, address='/tmp/dwm.sock') -> None:
        return super().connect(address)

    def send(self, msg_type: int, data=''):
        str_msg = json.dumps(data, ensure_ascii=True, separators=(',', ':'))
        msg_len = len(str_msg) + 1

        header = struct.pack(f'=7sIB', b'DWM-IPC', msg_len, msg_type)
        body = bytes(str_msg, 'utf-8') + b'\0'
        msg = header + body
        return super().send(msg)

    def recv(self):
        header = super().recv(12)
        assert len(header) == 12
        (magic, length, type) = struct.unpack('=7sIB', header)
        assert magic == b'DWM-IPC'
        msg_bytes = super().recv(length)
        msg_str = str(msg_bytes[:-1], 'utf-8')
        return json.loads(msg_str)

    def msg(self, msg_type: int, data=''):
        self.send(msg_type, data)
        return self.recv()

    def subscribe(self, event_name: str):
        req = {'event': event_name, 'action': 'subscribe'}
        res = self.msg(self.IPC_TYPE_SUBSCRIBE, req)
        assert (res.get('result') == 'success')

    def unsubscribe(self, event_name: str):
        req = {'event': event_name, 'action': 'unsubscribe'}
        res = self.msg(self.IPC_TYPE_SUBSCRIBE, req)
        assert (res.get('result') == 'success')
