# zetcd
A Juju charm for deploying zetcd as a replacement for zookeeper.

## Build

Known to build with:
```
charm 2.2.2
charm-tools 2.2.1
```
installed from snaps.

`./build.bash`

## Deploy

Known to work with Juju 2.2 in public clouds. Does not work when deployed to
LXD because snaps.

```
juju deploy cs:~containers/easyrsa
juju deploy cs:~containers/etcd
juju add-relation easyrsa etcd

juju deploy ./builds/zetcd
juju add-relation zetcd etcd

juju deploy kafka
juju add-relation zetcd kafka
```

