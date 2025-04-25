from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
  """A Node with IP forwarding enabled."""
  def config(self, **params):
    super(LinuxRouter, self).config(**params)
    self.cmd('sysctl -w net.ipv4.ip_forward=1')

  def terminate(self):
    self.cmd('sysctl -w net.ipv4.ip_forward=0')
    super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
  """"A LinuxRouter connecting three IP subnets.
  Args:
      Topo (Mininet.Topo): A Mininet Topography
  """
  def build(self, **_opts):
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


def add_router_routes(net):
  """Add all router's routes.
  Args:
      net (Mininet): Mininet network
  """
  info('*** Adding static routes to routers\n')

  net["rA"].cmd("ip route add 20.10.172.0/25 via 20.10.100.2")
  net["rA"].cmd("ip route add 20.10.172.192/27 via 20.10.100.6")

  net["rB"].cmd("ip route add 20.10.172.128/26 via 20.10.100.1")
  net["rB"].cmd("ip route add 20.10.172.192/27 via 20.10.100.3")

  net["rC"].cmd("ip route add 20.10.172.0/25 via 20.10.100.5")
  net["rC"].cmd("ip route add 20.10.172.128/26 via 20.10.100.4")


def add_host_routes(net):
  """Add all host's routers.
  Args:
      net (Mininet): Mininet network
  """
  info('*** Adding static routes to hosts\n')

  # hA1, hA2
  for h in ['hA1', 'hA2']:
    net[h].cmd("ip route add 20.10.172.0/25 via 20.10.172.129")
    net[h].cmd("ip route add 20.10.172.192/27 via 20.10.172.129")
  # hB1, hB2
  for h in ['hB1', 'hB2']:
    net[h].cmd("ip route add 20.10.172.128/26 via 20.10.172.1")
    net[h].cmd("ip route add 20.10.172.192/27 via 20.10.172.1")
  # hC1, hC2
  for h in ['hC1', 'hC2']:
    net[h].cmd("ip route add 20.10.172.128/26 via 20.10.172.193")
    net[h].cmd("ip route add 20.10.172.0/25 via 20.10.172.193")


def run():
  """Test linux router"""
  topo = NetworkTopo()
  net = Mininet(topo=topo, waitConnected=True)

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
  print("Pinging LAN A")
  net.ping([net['hA1'], net['hA2']])
  print("Pinging LAN B")
  net.ping([net['hB1'], net['hB2']])
  print("Pinging LAN C")
  net.ping([net['hC1'], net['hC2']])

  print("Task 2: Testing Connectivity before Inter-connectivity ")
  net.pingAll()

  # Static routing
  add_router_routes(net)
  add_host_routes(net)

  print("Testing full connectivity")
  net.pingAll()

  print("Traceroute from hA1 to hC1")
  print(net['hA1'].cmd("tracepath 20.10.172.194"))

  CLI(net)
  net.stop()

if __name__ == '__main__':
  setLogLevel('info')
  run()