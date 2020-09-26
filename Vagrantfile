# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "bento/ubuntu-16.04"

  config.vm.network :forwarded_port, guest: 9200, host: 9201, host_ip: "127.0.0.1"
  config.vm.network :forwarded_port, guest: 5601, host: 5602, host_ip: "127.0.0.1"

  config.vm.provider "virtualbox" do |vb|
     vb.memory = "4096"
     vb.name = "elkbox"
  end

  config.vm.provision "shell", inline: <<-END
  sudo apt-get update
  sudo apt-get install -y default-jdk
  sudo apt-get install unzip
  apt-get install python3-pip -y
  pip3 install pipenv
  echo '#!/bin/bash' > /home/vagrant/variables.sh
  chown vagrant:vagrant /home/vagrant/variables.sh
END

  for script in ['es_install.sh', 'kibana_install.sh', 'spark_install.sh', 'setup_demo_project.sh'] do
    script_path = "./bootstrap/install/#{script}"
    config.vm.provision "shell", privileged: false, path: script_path
  end

  config.vm.provision "shell", inline: <<-END
  SERVICE_FILES="/vagrant/bootstrap/services"
  cp ${SERVICE_FILES}/elasticsearch.service /etc/systemd/system/elasticsearch.service
  cp ${SERVICE_FILES}/kibana.service /etc/systemd/system/kibana.service
  systemctl daemon-reload
  systemctl enable elasticsearch
  systemctl enable kibana
  systemctl start elasticsearch
  systemctl start kibana
END

config.vm.synced_folder "bootstrap/", "/vagrant/bootstrap", disabled: true

end
