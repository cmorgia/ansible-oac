# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  

  config.vm.define 'ansible-vm' do |cfg|
    cfg.vm.box = 'abessifi/centos-7.1-ansible'
    cfg.vm.hostname = 'ansible-vm'
    cfg.vm.network 'private_network', ip: '192.168.33.101'
    cfg.vm.box_check_update = false
    cfg.vm.synced_folder '.', '/vagrantfolder', nfs: true
    cfg.vm.synced_folder '..', '/filesfolder', nfs: true
    cfg.vm.provider 'virtualbox' do |v|
      v.name = 'ansible-vm'
      v.cpus = 2
      v.memory = 4 * 1024
    end
    cfg.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'provision.yml'
      ansible.inventory_path = 'vagrant-inventory.ini'
      ansible.limit = 'ansible-vm'
      ansible.tags = 'install-java,wls-plain-install,oac-create-db-schemas,oac-install-and-init'
      ansible.verbose = 'v'
    end
  end

end
