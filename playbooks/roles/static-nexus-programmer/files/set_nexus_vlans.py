import os
import paramiko
import sys

nexus_ip = os.environ.get('NEXUS_IP')
nexus_user = os.environ.get('NEXUS_USER')
nexus_password = os.environ.get('NEXUS_PASSWORD')
nexus_intf_num = os.environ.get('NEXUS_INTF_NUM')
nexus_vlan_start = os.environ.get('NEXUS_VLAN_START')
nexus_vlan_end = os.environ.get('NEXUS_VLAN_END')


def clear_nexus_config(ip, user, password, intf_num, vlan_start, vlan_end,
                       vlan_native=None):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.connect(ip, username=user, password=password)

    parameters = [intf_num, vlan_start, vlan_end]

    cmd = ('config terminal ;'
           'interface Ethernet {0} ;'
           'switchport mode trunk ;')

    if vlan_native:
        cmd += ('switchport trunk native vlan {3} ;'
                'switchport trunk allowed vlan add {3} ;')
        parameters.append(vlan_native)

    cmd += ('switchport trunk allowed vlan add {1}-{2} ;'
            'vlan {1}-{2} ; ')

    if vlan_native:
        cmd += 'vlan {3}'

    cmd = cmd.format(*parameters)
    print cmd
    stdin, stdout, stderr = client.exec_command(cmd)
    print stdout.readlines()
    client.close()


def print_usage():
    print "Usage:"
    print "    python %s <nexus-ip> <user> <password> " % sys.argv[0]
    print "              <intf-num> <vlan-start> <vlan-end> <vlan-native>"
    print "Example:"
    print "    python %s 10.0.1.32 admin MyPassword 1/9 810 813" % sys.argv[0]
    print "Note: VLAN range is inclusive."
    print "Note: Number of VLANs in VLAN range should not exceed 100."

if __name__ == '__main__':
    if "--help" in sys.argv:
        print_usage()
        sys.exit(0)
    if (len(sys.argv) != 7 and
            len(sys.argv) != 8):
        print_usage()
        sys.exit(1)
    if len(sys.argv) == 7:
        clear_nexus_config(sys.argv[1], sys.argv[2], sys.argv[3],
                           sys.argv[4], sys.argv[5], sys.argv[6])
    if len(sys.argv) == 8:
        clear_nexus_config(sys.argv[1], sys.argv[2], sys.argv[3],
                           sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
