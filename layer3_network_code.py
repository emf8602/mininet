"""
layer3_network_code.py largely inspired from linuxrouter.py in mininet examples
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
  "A Node with IP forwarding enabled."

  # pylint: disable=arguments-differ
  def config( self, **params ):
    super( LinuxRouter, self).config( **params )
    # Enable forwarding on the router
    self.cmd( 'sysctl net.ipv4.ip_forward=1' )

  def terminate( self ):
    self.cmd( 'sysctl net.ipv4.ip_forward=0' )
    super( LinuxRouter, self ).terminate()
  
class NetworkTopo( Topo ):
  "A LinuxRouter connecting three IP subnets"

  # pylint: disable=arguments-differ
  def build( self, **_opts ):
    print("TODO")
    
    # Populate topology with routers, LANs , Switches, and links


def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo, waitConnected=True )
    net.start()
    
    # Testing connections between hosts in a lan
    
    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()