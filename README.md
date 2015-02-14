aws-nagiosplugin
==========

A simple Nagios plugin for Amazon EC2 services
Nagios supports a way to monitor hosts and services passively instead of actively. Passive checks are initiated and performed by external applications/processes.

![alt tag](http://nagios.sourceforge.net/docs/3_0/images/externalcommands.png)


## Nagios configuration

edit /etc/nagios3/nagios.cfg
```
check_external_commands=1
command_file=/var/lib/nagios3/rw/nagios.cmd
```
edit /etc/nagios3/commands.cfg

```
define command{
        command_name    check_dummy
        command_line    /usr/lib/nagios/plugins/check_dummy ‘$ARG1$’ ‘$ARG2$
        }
```

edit /etc/nagios3/passive-service.cfg

```
define service{
        name                    passive-service
        use                     generic-service
        check_freshness         1
        passive_checks_enabled  1
        active_checks_enabled   0
        is_volatile             0
        flap_detection_enabled  0
        freshness_threshold     57600     ;12hr
}
```

edit /etc/nagios3/conf.d/nagios-manager.cfg

```
define service{
        use                             passive-service
        host_name                       interact-manager
        check_command                   check_dummy!3!”Dati non ricevuti”
        service_description             AWS Storage Usage
        contact_groups                  Sistemi,Reperibile
}
```

Test

```
python /root/aws/checkebs-nagios.py > /var/lib/nagios3/rw/nagios.cmd
```
