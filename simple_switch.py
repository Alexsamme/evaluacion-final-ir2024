# simple_switch.py
from ryu.base import app_manager
from ryu.controller import controller
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import Event
from ryu.lib.packet import ethernet
from ryu.ofproto import ofproto_v1_3

class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    @set_ev_cls(Event, MAIN_DISPATCHER)
    def handle_event(self, event):
        # Maneja eventos de red, como la llegada de paquetes
        pass