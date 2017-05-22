import os

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charms.reactive import hook, when, when_not, is_state, set_state, remove_state


@when('zookeeper.ready')
def setup_zk(zk):
    zk.send_connection(2181, 2181)


@when('etcd.available')
def setup_etcd(etcd):
    # TODO: write cert files if TLS enabled
    render(source="zetcd.service",
        target='/etc/systemd/system/zetcd.service',
        owner='root',
        mode=0o755,
        context={
            'zk_port': 2181,
            'etcd_endpoint': etcd.connection_string(),
        })
    if host.service_running('zetcd'):
        host.service_restart('zetcd')
    else:
        host.service_start('zetcd')
    hookenv.open_port(2181)
    hookenv.status_set('active', 'zetcd running')


@when_not('etcd.available')
def wants_etcd():
    if host.service_available('zetcd') and host.service_running('zetcd'):
        host.service_stop('zetcd')
    hookenv.close_port(2181)
    try:
        os.unlink('/etc/systemd/system/zetcd.service')
    except:
        pass
    hookenv.status_set('blocked', 'waiting for relation to etcd')
