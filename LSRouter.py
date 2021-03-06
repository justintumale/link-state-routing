import socket
import ForwardEchoListener
import LinkStateListener
import LinkMessageBroadcast
import OverlayGraph
import OverlayGraphMonitor
import time


class LSRouter:
    host = ''
    LM_receive_port = ''
    LM_receive_socket = ''
    forward_echo_port = ''
    forward_echo_socket = ''
    broadcast_socket = ''

    #creates an instance of the Overlay Graph class
    OVERLAY_GRAPH = OverlayGraph.OVERLAY_GRAPH
    #spoof graph
    '''
    OverlayGraph.create_link('fjt14188', 'kamercer', 9000000000000)
    OverlayGraph.create_link('fjt14188', 'mwong9', 9000000000000)
    OverlayGraph.create_link('fjt14188', 'trsturbo', 9000000000000)
    OverlayGraph.create_link('kamercer', 'fjt14188', 9000000000000)
    OverlayGraph.create_link('mwong9', 'fjt14177', 9000000000000)
    OverlayGraph.create_link('trsturbo', 'fjt14188', 9000000000000)
    OverlayGraph.create_link('kamercer', 'cannan', 9000000000000)
    OverlayGraph.create_link('mwong9', 'kamercer', 9000000000000)
    OverlayGraph.create_link('trsturbo', 'bbreyel', 9000000000000)
    OverlayGraph.create_link('bbreyel', 'cannan', 9000000000000)
    '''

    #maps student nodes to their ports
    NODE_PORT_MAP = {'student0' : [20020,   20021],
                    'kbadams'   : [21020,   21021],
                    'jadolphe'  : [21120,   21121],
                    'cannan'    : [21220,   21221],
                    'mbamaca'   : [21320,   21321],
                    'adb2016'   : [21420,   21421],
                    'bbreyel'   : [21520,	21521],
                    'derosa30'  : [21620,	21621],
                    'ddiener'	: [21720,	21721],
                    'foretich'	: [21820,	21821],
                    'coal175'	: [21920,	21921],
                    'reiner'	: [22020,	22021],
                    'ahayes44'	: [22120,	22121],
                    'ahiggins'	: [22220,	22221],
                    'da3nvy'	: [22320,	22321],
                    'yd9'	    : [22420,	22421],
                    'hjink94'	: [22520,	22521],
                    'stevenk'	: [22620,	22621],
                    'bruceli'	: [22720,	22721],
                    'mattling'	: [22820,	22821],
                    'erlock'	: [22920,	22921],
                    'alexms'	: [23020,	23021],
                    'brandonm'	: [23120,	23121],
                    'jarmac76'	: [23220,	23221],
                    'kamercer'	: [23320,	23321],
                    'dylmorg'	: [23420,	23421],
                    'nikolich'	: [23520,	23521],
                    'mbp1988'	: [23620,	23621],
                    'lpastor'	: [23720,	23721],
                    'rpersaud'	: [23820,	23821],
                    'jplizzle'	: [23920,	23921],
                    'tonyr'	    : [24020,	24021],
                    'mreece05'	: [24120,	24121],
                    'rucker21'	: [24220,	24221],
                    'quintezs'	: [24320,	24321],
                    'jls93'	    : [24420,	24421],
                    'kds'	    : [24520,	24521],
                    'trsturbo'	: [24620,	24621],
                    'fjt14188'	: [24720,	24721],
                    'lvanhuss'	: [24820,	24821],
                    'lucyv'	    : [24920,	24921],
                    'vinsonj'	: [25020,	25021],
                    'jakewebb'	: [25120,	25121],
                    'whatleym'	: [25220,	25221],
                    'wilbur13'	: [25320,	25321],
                    'mwong9'	: [25420,	25421],
                    'byang9'	: [25520,	25521],
                    'dilawarz'	: [25620,	25621]}

    #create the links to connect to
    LINKS = ['kamercer', 'trsturbo', 'mwong9', 'ahiggins']
    OverlayGraph.create_link('fjt14188', 'kamercer', int(time.time())+120 )
    OverlayGraph.create_link('fjt14188', 'mwong9', int(time.time())+120 )
    OverlayGraph.create_link('fjt14188', 'trsturbo', int(time.time())+120 )
    OverlayGraph.create_link('fjt14188', 'ahiggins', int(time.time())+120 )



    def __init__(self):
        self.host = "127.0.0.1"

        self.LM_receive_port = 24720
        self.LM_receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.LM_receive_socket.bind((self.host, self.LM_receive_port))

        self.forward_echo_port = 24721
        self.forward_echo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.forward_echo_socket.bind((self.host, self.forward_echo_port))

        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def run(self):
        '''Runs the listeners to handle concurrent sending/receiving of messages.  It also runs
        the OverlayGraphMonitor, which is responsible for deleting dead links from the Overlay
        Graph.'''
        print('Running router...')


        LMListener = LinkStateListener.LinkStateListener(self.LM_receive_socket, self.OVERLAY_GRAPH)
        LMListener.start()

        overlay_graph_monitor = OverlayGraphMonitor.OverlayGraphMonitor()
        overlay_graph_monitor.start()

        FEListener = ForwardEchoListener.ForwardEchoListener(self.forward_echo_socket, self.LINKS, self.NODE_PORT_MAP)
        FEListener.start()

        Broadcaster = LinkMessageBroadcast.LinkMessageBroadcast(self.host, self.LM_receive_socket,
                                                                self.NODE_PORT_MAP, self.LINKS)
        Broadcaster.start()

        LMListener.join()
        overlay_graph_monitor.join()
        FEListener.join()
        Broadcaster.join()

        self.LM_receive_socket.close()
        self.forward_echo_socket.close()


def Main():
    a = LSRouter()
    a.run()


if __name__ == '__main__':
    Main()