Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.vbguest.auto_update = false
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip nano tree
  SHELL
end
