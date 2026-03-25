Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.vbguest.auto_update = false
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip nano tree
    chmod +x /vagrant/lsit.py
    ln -s /vagrant/lsit.py /usr/local/bin/lsit
    # Création de la tâche planifiée (Tous les jours à minuit, en format JSON)
    echo "0 0 * * * root /usr/local/bin/lsit --format json" > /etc/cron.d/lsit_audit
  SHELL
end
