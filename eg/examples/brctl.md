# brctl

## Basic usage

List all bridges:

    brctl show

Create bridge `br1`:

    brctl addbr br1

Add interface `eth0` to bridge `br1`:

    brctl addif br1 eth0

Delete interface `eth0` from bridge `br1`:

    brctl delif br1 eth0

Delete bridge `br1`:

    brctl delbr br1

## Advanced usage

Show MAC addresses learned by bridge `br1` and port from which they were learned:

    brctl showmacs br1

Turn on STP on bridge `br1`:

    brctl stp br1 on

Setup ageing of MAC addresses in bridge `br1` to 0 seconds. This will cause bridge to not learn MAC addresses:

    brctl setageing br1 0

Show details about bridge `br1`:

    brctl showstp br1
