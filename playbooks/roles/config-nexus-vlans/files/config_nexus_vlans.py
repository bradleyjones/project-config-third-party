import paramiko
import sys


def nexus_config(ip, user, password, op, intf_num, vlan_start, vlan_end):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.connect(ip, username=user, password=password)
    cmd = 'config terminal ; '
    if op == 'remove':
        cmd += 'no '
    cmd += ('vlan {0}-{1} ; ').format(vlan_start, vlan_end)
    cmd += ('interface Ethernet {0} ; '
            'switchport trunk allowed vlan {3} {1}-{2} ; '
            ).format(intf_num, vlan_start, vlan_end, op)
    print cmd
    stdin, stdout, stderr = client.exec_command(cmd)
    print stdout.readlines()
    client.close()


def print_usage():
    print "Usage:"
    print "    python %s <nexus-ip> <user> <password> " % sys.argv[0]
    print "              [add|remove] <intf-num> <vlan-start> <vlan-end>"
    print "Example:"
    print "    python %s 10.0.1.32 admin MyPassword 1/9 810 813" % sys.argv[0]
    print "Note: VLAN range is inclusive."
    print "Note: Number of VLANs in VLAN range should not exceed 100."

if __name__ == '__main__':
    if "--help" in sys.argv:
        print_usage()
        sys.exit(0)
    if len(sys.argv) != 8:
        print_usage()
        sys.exit(1)
    nexus_config(sys.argv[1], sys.argv[2], sys.argv[3],
                 sys.argv[4], sys.argv[5], sys.argv[6],
                 sys.argv[7])
