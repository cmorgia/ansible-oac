# Ansible OAC Role

## Description

This is an Ansible role to install and configure Oracle Service Bus 12c.

## Supported systems

- CentOS 7

## Role dependencies

- [ansible-java](https://github.com/abessifi/ansible-java)
- [ansible-weblogic](https://github.com/abessifi/ansible-weblogic)

## Requirements

### Software Requirements

- **Ansible 1.9** or higher (can be easily installed via `pip`. E.g: `sudo pip install ansible==1.9.2`)
- **[Vagrant](https://www.vagrantup.com) 1.7** or higher
- `sshpass` package which is needed by Ansible if you are using SSH authentication by password. On Ubuntu/Debian: `$ sudo apt-get install sshpass`
- **Virtualbox**
- **[Oh-my-box](https://github.com/abessifi/oh-my-box)** tool, optional, if you want to quickly provision and package a Vagrant base box with **Ansible** and **Ruby** pre-installed.

### System requirements

- **Oracle JDK 8** (see [ansible-java](https://github.com/abessifi/ansible-java))

- **Fusion Middleware Infrastructure 12c Plateform**. You can download the installer JAR file `fmw_12.2.1.0.0_infrastructure.jar` from the [Oracle Software Delivery Cloud](https://edelivery.oracle.com), put it somewhere in the machine(s) to provision and use the [ansible-weblogic](https://github.com/abessifi/ansible-weblogic) role to install and configure a WebLogic platform.

- **Oracle Service Bus** installer JAR file `fmw_12.2.1.0.0_oac.jar` which can be obtained from the [Oracle Software Delivery Cloud](https://edelivery.oracle.com).

- An access to an Oracle 12c Database is required too in order to create the OAC essential schemas using RCU tool (the role should work with an Oracle 11g DB also).

### Memory requirements

The specific memory requirements for your Oracle Service Bus 12c deployment depends on which components, or combination of components, you install. Please read the Oracle Fusion Middleware installation guidelines for more details about memory requirements.

In case of a plain installation using this Ansible role such as a combination of a nodemanager, an AdminServer and one Managed Server in the same server, the required memory is at least **4GB** of physical memory and **1GB** of Swap space.

## Role Variables

#### OAC installation parameters

- **`oracle_base_dir`** - The Oracle base directory (default: `/u01/app/oracle`)
- **`middleware_home_dir`** - The Oracle Middleware installation directory (default: `/u01/app/oracle/product/middleware`)
- **`oac_installation_type`** - The Oracle Service Bus installation type (default: `'Service Bus'`)
- **`oac_jar_path`** - Required absolute path to the OAC installer JAR file (default: `''`)
- **`oac_version`** - The OAC version to install (default: `12c`)
- **`oac_already_installed`** - A Flag to indicate if OAC is already installed (default: `false`)
- **`oac_schemas_created`** - A Flag to tell if the OAC schemas are installed or not (default: `false`)

#### Oracle database connection parameters

- **`oracle_db_address`** - A required Oracle database address (default: `localhost`)
- **`oracle_db_port`** - The Oracle database connection port (default: `1521`)
- **`oracle_db_sid`** - A required Oracle database connection system identifier (default: `xe`)
- **`oracle_db_user`** - The Oracle database admin user name (default: `sys`)
- **`oracle_db_password`** - A required Oracle database admin user password (default: `oracle`)
- **`oracle_db_role`** - The Oracle database admin user role (default: `SYSDBA`)

#### OAC database schemas

- **`oac_rcu_components`** - The OAC schemas components to install (default: `[ MDS, IAU, IAU_APPEND, IAU_VIEWER, OPSS, UCSUMS, WLS, STB, SOAINFRA ]`)
- **`oac_rcu_schema_prefix`** - The OAC database schemas prefix (default: `OAC`)
- **`oac_schemas_common_password`** - Required OAC schemas common password (default: `oracle`)

#### Cluster parameters

- **`oac_domain_name`** -  The OAC WebLogic domain name (default: `oac_domain`)
- **`oac_cluster_name`** - The OAC cluster name (default: `oac_cluster`)
- **`oac_cluster_nodes`** - The OAC cluster nodes/machines (default: `["{{ ansible_fqdn }}"]`)

#### OAC NodeManager parameters

- **`oac_nodemanager_listen_address`** - The NodeManager listening address (default: `localhost`)
- **`oac_nodemanager_listen_port`** -  The NodeManager listening port (default: `5556`)
- **`oac_nodemanager_connection_mode`** - The NodeManager's connection mode (default: `ssl`)

#### OAC AdminServer parameters

- **`oac_admin_server_name`** - The AdminServer instance name (default: `AdminServer`)
- **`oac_admin_server_listen_address`** - The AdminServer listening address (default: `"{{ ansible_fqdn }}"`)
- **`oac_admin_server_listen_port`** - The AdminServer listening port (default: `7001`)
- **`oac_admin_username`** - The WebLogic administrator user name (default: `weblogic`)
- **`oac_admin_password`** - The WebLogic administrator user password (default: `manager1`)

#### OAC NodeManager parameters

- **`oac_managed_servers_per_machine`** - The maximum number of managed servers per machine (default: `1`)
- **`oac_managed_server_listen_port_start`** - The managed servers start listening port number (default: `8000`)
- **`oac_managed_server_listen_address`** - The managed servers listen address (default: `"{{ ansible_fqdn }}"`)

#### JVM heap parameters

- **`oac_admin_server_heap_size`** - The AdminServer heap size (default: `512m`)
- **`oac_admin_server_perm_size`** - The AdminServer permanent generation size (default: `256m`)
- **`oac_managed_server_heap_size`** - The Managed server heap size (default: `1024m`)
- **`oac_managed_server_perm_size`** - The Managed server permanent generation size (default: `512m`)
- **`oac_coherence_server_heap_size`** -  The Coherence server heap size (default: `256m`)
- **`oac_coherence_server_perm_size`** - The Coherence server permanent generation size (default: `128m`)

#### Import OAC project parameters

- **`oac_sbconfig_jar_file`** - Path to the OAC project's JAR file to be imported (default: `/tmp/sbconfig.jar`)
- **`oac_sbconfig_customization_file`** - Path to the OAC project's customization XML file to be applied (default: `/tmp/ALSBCustomizationFile.xml`)

## Available tags

- **`oac-create-db-schemas`** - Specify this tag to create the OAC schemas using RCU.
- **`oac-purge-db-schemas`** - Use this tag if you want to purge an existing OAC schemas to prepare for a clean installation. If you want that the purge take effect, you have to set the role parameter `oac_schemas_created` to `true`. The role parameters for db connection, the schemas prefix and the RCU components are required too.
- **`oac-plain-install`** - This tag performs only the installation of the OAC software.
- **`oac-configure`** - When mentioned, the OAC configuration tasks are executed (Create OAC cluster, etc).
- **`oac-install-and-init`** - This is the default installation mode of the OAC. When mentioned, this tag performs the creation of a new domain, the configuration and startup of an OAC cluster with 3 services: a nodemanager, an AdminServer and one Manager Server.
- **`oac-start-nodemanager`** - Starts the nodemanager service.
- **`oac-stop-nodemanager`** - Stops the nodemanager service.
- **`oac-restart-nodemanager`** - Restarts the nodemanager service.
- **`oac-start-adminserver`** - Starts the AdminServer process.
- **`oac-stop-adminserver`** - Stops the AdminServer process.
- **`oac-start-managed-servers`** - Starts the Managed Servers processes.
- **`oac-stop-managed-servers`** - Stops the Managed Servers processes.
- **`oac-import-project`** - Import existing OAC project.

## Local facts

- **`oac.db.created`** - Tell if the OAC schemas are installed or not

# Usage

### Oracle database setup

Personally and for quick tests, I use the Docker image [sath89/oracle-12c](https://hub.docker.com/r/sath89/oracle-12c/) that brings up an Oracle 12c database server. All you need is to pull the image, create a local data directory and spin up an `oracle-db` container:

	$ sudo docker pull sath89/oracle-12c:latest
	$ sudo mkdir -p /var/lib/oracledb/data
    $ sudo docker run --name oracle-db -d -p 8080:8080 -p 1521:1521 -v /var/lib/oracledb/data:/u01/app/oracle -e DBCA_TOTAL_MEMORY=1024 sath89/oracle-12c

To test the database connection:

	$ sqlplus -L sys/oracle@db.weblogic.local/xe.oracle.docker as sysdba

	Connected to:
	Oracle Database 12c Standard Edition Release 12.1.0.2.0 - 64bit Production

	SQL>


### All from scratch

First, download Oracle JDK 8 rpm, Fusion Middleware Infrastructure and OAC 12c installer JARs and put them somewhere in the server to provision. Below an example:

	$ ls -1 /srv/files/
	fmw_12.2.1.0.0_infrastructure.jar
	fmw_12.2.1.0.0_oac.jar
	jdk-8u77-linux-x64.rpm

Next, clone this project and download the required Ansible roles to install and configure the Oracle JDK and the WebLogic platform:

	$ sudo ansible-galaxy install -p /etc/ansible/roles/ -r requirements.txt

To install an Oracle Service Bus Infrastructure (that uses Oracle JDK 8 as the Java Virtual Machine) you can use the following `provision.yml` playbook:

```yaml
- hosts: my-server
  roles:
    - role: abessifi.java
      sudo: yes
      java_version: 8
      java_jdk_type: 'oracle'
      oracle_jdk_rpm_package: 'jdk-8u77-linux-x64.rpm'
      rpm_download_directory: '/srv/files'
      java_set_as_default: true
      tags:
        - install-java

    - role: abessifi.weblogic
      weblogic_jar_path: '/srv/files/fmw_12.2.1.0.0_infrastructure.jar'
      weblogic_quick_installation: false
      weblogic_installation_type: 'Fusion Middleware Infrastructure'
      weblogic_domain_name: 'oac_domain'

    - role: ansible-oac
      oac_jar_path: '/srv/files/fmw_12.2.1.0.0_oac.jar'
      oracle_db_address: 'db.weblogic.local'
      oracle_db_sid: 'xe.oracle.docker'
      oracle_db_password: 'oracle'
      oac_schemas_common_password: 'oracle'
      oac_domain_name: 'oac_domain'
      oac_admin_server_listen_address: 'oac.weblogic.local'
      oac_managed_server_listen_address: 'oac.weblogic.local'
```

That's all ! It's now time to call Ansible to provision your server. Here is an example of ansible-playbook command:

	$ ansible-playbook --user=<user-name> --connection=ssh --timeout=30 --inventory-file=inventory.ini --tags='install-java,wls-plain-install,oac-plain-install' -v provision.yml

**Notes:**

- In the above playbook example, the `db.weblogic.local` refers to the host machine where the oracle database is installed and the `oac.weblogic.local` is the FQDN of the server we are provisioning.
- Make sure you have updated `/etc/hosts` file, so the FQDNs `db.weblogic.local` and `oac.weblogic.local` can be resolved correctly. Otherwise, replace the FQDNs by IP address in the playbook.
- You need to create and adapt the Ansible inventory files and variables to suit your environment (services ports, IP addresses, etc)

### Import OAC project

You can use the magic tag `oac-import-project` to import an existing OAC project exported as a JAR file and apply a customization file to adapt the OAC platform to feet the required configuration. To do so you have just to specify the input project JAR and XML customization files:

```yaml
- hosts: ansible-vm
  roles:
    - role: ansible-oac
      oac_sbconfig_jar_file: '/srv/files/oac_cabestan.jar'
      oac_sbconfig_customization_file: '/srv/files/ALSBCustomizationFile_cabestan.xml'
```

	$ ansible-playbook --user=<user-name> --connection=ssh --timeout=30 --inventory-file=inventory.ini --tags='oac-import-project' -v provision.yml

**Notes:**
- Mainly the OAC 11g projects may be imported to the 12c platform.
- If importation fails, take a look to the default log file `/home/oracle/logs/oac_import_project_<timestamp>.log` to identify the failure root reason.

### Purge existing OAC schemas

If you want to purge an existing OAC schemas and start a clean installation, use the Ansible tags `oac-purge-db-schemas` and set the role parameter `oac_schemas_created` to remove the schemas from the Oracle database before recreating them during installation process:

	$ ansible-playbook --user=<user-name> --connection=ssh --timeout=30 --inventory-file=inventory.ini --tags='install-java,wls-plain-install,oac-purge-db-schemas,oac-plain-install' -v provision.yml

### Installation on top of an existing WebLogic platform

The installation is kept straightforward even with a such use case ! Just specify the **absolute path** of the Oracle Middleware installation directory using the `middleware_home_dir` parameter:

```yaml
- hosts: my-server
  roles:

    - role: ansible-oac
      oac_jar_path: '/srv/files/fmw_12.2.1.0.0_oac.jar'
      oracle_db_address: 'db.weblogic.local'
      oracle_db_sid: 'xe.oracle.docker'
      oracle_db_password: 'oracle'
      oac_schemas_common_password: 'oracle'
      middleware_home_dir: '/u01/app/oracle/product/middleware_12.2.1'
      oac_domain_name: 'oac_domain'
      oac_admin_server_listen_address: 'oac.weblogic.local'
      oac_managed_server_listen_address: 'oac.weblogic.local'
```

	$ ansible-playbook --user=<user-name> --connection=ssh --timeout=30 --inventory-file=inventory.ini --tags='oac-plain-install' -v provision.yml

Note that the only passed Ansible tag to perform the installation is `oac-plain-install`.

### Restart cluster services

In case of problem with the WebLogic instances, you can restart the chain service by restarting the Nodemanager service "the entrypoint":

	$ ansible-playbook --user=<user-name> --connection=ssh --timeout=30 --inventory-file=inventory.ini --tags='oac-restart-nodemanager' -v provision.yml

# Development and testing

## Test with Vagrant

For quick tests, you can spin-up a CentOS VM using Vagrant. You maybe need to adapt the Vagrantfile to suit your environment (IP addresses, etc):

- Change the Vagrant box name in the Vagrantfile if needed.

- Create the virtual machine:
```
(host)$ vagrant up --no-provision
```
- Update the `/etc/hosts` in the host machine and the VM accordingly to reach the addresses `db.weblogic.local` and `oac.weblogic.local`:
```
	<db-server-address>   db.weblogic.local
	<oac-server-address>  oac.weblogic.local
```
- Create a working directory to copy installer files to:
```
	[vagrant@ansible-vm ~]$ sudo mkdir /srv/files/ && sudo chown vagrant:vagrant /srv/files/
```
- Copy downloaded installer JAR files:
```
	(host)$ rsync -iav /path/to/{fmw_12.2.1.0.0_infrastructure.jar,jdk-8u77-linux-x64.rpm,fmw_12.2.1.0.0_oac.jar} vagrant@oac.weblogic.local:/srv/files/
```
- Download the required Ansible roles to install and configure the Oracle JDK and the WebLogic platform (not required if your box is already provision):
```
	(host)$ sudo ansible-galaxy install -p /etc/ansible/roles/ -r requirements.txt
```
- Install all stuff !
```
	(host)$ vagrant provision
```

## Run acceptance tests

Acceptance/Integration tests could be run against the role using the magic `test-kitchen` tool. All the written acceptance tests are in the **./test/integration/** directory.

The `.kitchen.yml` file describes the testing configuration and the list of tests suite to run. By default, your instances will be converged with Ansible and run in Vagrant virtual machines.

To list the instances:

    $ kitchen list

    Instance                    Driver   Provisioner      Verifier  Transport  Last Action
    default-centos-7-x64        Vagrant  AnsiblePlaybook  Busser    Ssh        <Not Created>

To run the default test suite on a CentOS 7 platform, run the following:

    $ kitchen test

## Author

This role was created by [Ahmed Bessifi](https://www.linkedin.com/in/abessifi), a DevOps enthusiast.
