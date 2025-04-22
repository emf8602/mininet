"""layer3_network_code.py based on linuxrouter.py in mininet examples"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
  """A Node with IP forwarding enabled."""

  # pylint: disable=arguments-differ
  def config( self, **params ):
    super( LinuxRouter, self).config( **params )
    # Enable forwarding on the router
    self.cmd( 'sysctl self.ipv4.ip_forward=1' )

  def terminate( self ):
    self.cmd( 'sysctl self.ipv4.ip_forward=0' )
    super( LinuxRouter, self ).terminate()
  


class NetworkTopo( Topo ):
  """"A LinuxRouter connecting three IP subnets.
  Args:
      Topo (Mininet.Topo): A Mininet Topography
  """
  # pylint: disable=arguments-differ
  def build( self, **_opts ):
    """Populate topology with routers, LANs, Switches, and Links."""
    
    info('*** Adding routers\n')
    rA = self.addHost('rA', cls=LinuxRouter, ip='20.10.172.129/26')
    rB = self.addHost('rB', cls=LinuxRouter, ip='20.10.172.1/25')
    rC = self.addHost('rC', cls=LinuxRouter, ip='20.10.172.193/27')

    info('*** Adding LAN hosts\n')
    hA1 = self.addHost('hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
    hA2 = self.addHost('hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')

    hB1 = self.addHost('hB1', ip='20.10.172.2/25', defaultRoute='via 20.10.172.1')
    hB2 = self.addHost('hB2', ip='20.10.172.3/25', defaultRoute='via 20.10.172.1')

    hC1 = self.addHost('hC1', ip='20.10.172.194/27', defaultRoute='via 20.10.172.193')
    hC2 = self.addHost('hC2', ip='20.10.172.195/27', defaultRoute='via 20.10.172.193')

    info('*** Creating switches\n')
    sA = self.addSwitch('s1')
    sB = self.addSwitch('s2')
    sC = self.addSwitch('s3')

    info('*** Connecting LANs to routers\n')
    self.addLink(hA1, sA)
    self.addLink(hA2, sA)
    self.addLink(rA, sA, intfName1='rA-eth0')

    self.addLink(hB1, sB)
    self.addLink(hB2, sB)
    self.addLink(rB, sB, intfName1='rB-eth0')

    self.addLink(hC1, sC)
    self.addLink(hC2, sC)
    self.addLink(rC, sC, intfName1='rC-eth0')

    info('*** Connecting routers to each other\n')
    self.addLink(rA, rB, intfName1='rA-eth1', intfName2='rB-eth1')
    self.addLink(rB, rC, intfName1='rB-eth2', intfName2='rC-eth1')
    self.addLink(rC, rA, intfName1='rC-eth2', intfName2='rA-eth2')

def run():
  "Test linux router"
  topo = NetworkTopo()
  net = Mininet( topo=topo, waitConnected=True )
  
  info('*** Starting Network\n')
  net.start()
  
  info('*** Assigning IPs\n')
  net["rA"].setIP('20.10.100.1/24', intf='rA-eth1')
  net["rA"].setIP('20.10.100.4/24', intf='rA-eth2')

  net["rB"].setIP('20.10.100.2/24', intf='rB-eth1')
  net["rB"].setIP('20.10.100.5/24', intf='rB-eth2')

  net["rC"].setIP('20.10.100.3/24', intf='rC-eth1')
  net["rC"].setIP('20.10.100.6/24', intf='rC-eth2')
  
  # Testing connections between hosts in a lan
  print("\n--- Testing LAN A ---")
  net.ping([net["hA1"], net["hA2"]])

  print("\n--- Testing LAN B ---")
  net.ping([net["hB1"], net["hB2"]])

  print("\n--- Testing LAN C ---")
  net.ping([net["hC1"], net["hC2"]])

  info('*** Opening Mininet CLI\n')
  
  CLI( net )
  net.stop()


if __name__ == '__main__':
  """Sets logs to 'info' and executes the network code"""
  setLogLevel( 'info' )
  run()