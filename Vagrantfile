Vagrant.configure("2") do |config|

  # ─── Machine Debian 12 ────────────────────────────────────────────────────────
  config.vm.define "debian", primary: true do |debian|
    debian.vm.box = "debian/bookworm64"
    debian.vbguest.auto_update = false
    debian.vm.network "forwarded_port", guest: 5000, host: 8081

    debian.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y python3 python3-pip nano tree python3-flask

      # Supprimer les retours chariot Windows (\r)
      sed -i 's/\r$//' /vagrant/lsit.py \
        /vagrant/Moteur/base/moteur_base.py \
        /vagrant/Moteur/linux/moteur_linux.py

      chmod +x /vagrant/lsit.py
      ln -sf /vagrant/lsit.py /usr/local/bin/lsit
      echo "0 0 * * * root /usr/local/bin/lsit --format json" > /etc/cron.d/lsit_audit
      cat > /etc/profile.d/lsit-welcome.sh << 'EOF'
#!/bin/bash
[[ $- == *i* ]] || return

while true; do
  echo ""
  echo "  ╔══════════════════════════════════════════╗"
  echo "  ║   LSIT - Linux System Inventory Tool     ║"
  echo "  ╚══════════════════════════════════════════╝"
  echo ""
  echo "    [1]  Interface graphique  (port 8081)"
  echo "    [2]  Rapport TXT"
  echo "    [3]  Rapport JSON"
  echo "    [4]  Shell uniquement"
  echo "    [5]  Quitter"
  echo ""
  read -rp "  Votre choix [1-5] : " lsit_choix

  case "$lsit_choix" in
    1)
      echo ""
      echo "  Démarrage du tableau de bord..."
      echo "  --> Ouvre http://localhost:8081 dans ton navigateur."
      echo '  Tapez "exit" ou "end" pour arrêter et revenir ici.'
      echo ""
      lsit --serve
      ;;
    2)
      echo ""
      lsit --format txt
      ;;
    3)
      echo ""
      lsit --format json
      ;;
    4)
      echo ""
      echo "  Commandes disponibles :"
      echo "    lsit --format txt   --> rapport TXT"
      echo "    lsit --format json  --> rapport JSON"
      echo "    lsit --serve        --> tableau de bord web (port 8081)"
      echo ""
      break
      ;;
    5|exit|end)
      echo ""
      exit
      ;;
    *)
      echo "  Choix invalide. Veuillez entrer 1, 2, 3, 4 ou 5."
      ;;
  esac
done
EOF
      chmod +x /etc/profile.d/lsit-welcome.sh
    SHELL
  end

  # ─── Machine FreeBSD 14 ───────────────────────────────────────────────────────
  config.vm.define "freebsd" do |freebsd|
    freebsd.vm.box = "generic/freebsd14"
    freebsd.vm.network "forwarded_port", guest: 5000, host: 8082

    # rsync requis : les VirtualBox Guest Additions sont instables sur FreeBSD
    freebsd.vm.synced_folder ".", "/vagrant", type: "rsync",
      rsync__exclude: [".git/", ".vagrant/", "__pycache__/"]

    freebsd.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus   = 1
    end

    freebsd.vm.provision "shell", inline: <<-SHELL
      # Mise à jour du gestionnaire de paquets
      pkg update -q

      # Installation des dépendances (bash requis pour le menu interactif)
      pkg install -y python3 tree bash

      # Bootstrap pip puis Flask
      python3 -m ensurepip --upgrade 2>/dev/null || true
      python3 -m pip install --quiet flask

      # Supprimer les retours chariot Windows (\r) des scripts Python
      # rsync depuis Windows envoie des fichiers CRLF qui cassent le shebang sur FreeBSD
      sed -i '' 's/\r$//' /vagrant/lsit.py /vagrant/Moteur/base/moteur_base.py /vagrant/Moteur/linux/moteur_linux.py /vagrant/Moteur/freebsd/moteur_freebsd.py

      # Rendre lsit exécutable et accessible globalement
      chmod +x /vagrant/lsit.py
      ln -sf /vagrant/lsit.py /usr/local/bin/lsit

      # Cron : rapport JSON quotidien à minuit
      echo "0 0 * * * root /usr/local/bin/lsit --format json" > /etc/cron.d/lsit_audit
      service cron restart

      # Changer le shell de vagrant en bash (pw usermod est la méthode native FreeBSD)
      pw usermod vagrant -s /usr/local/bin/bash

      # Menu dans .bash_profile : FreeBSD ne source pas /etc/profile.d/ au login,
      # contrairement à Debian. .bash_profile est toujours chargé par bash login.
      cat > /home/vagrant/.bash_profile << 'EOF'
[[ $- == *i* ]] || return

while true; do
  echo ""
  echo "  ╔══════════════════════════════════════════╗"
  echo "  ║   LSIT - FreeBSD System Inventory Tool   ║"
  echo "  ╚══════════════════════════════════════════╝"
  echo ""
  echo "    [1]  Interface graphique  (port 8082)"
  echo "    [2]  Rapport TXT"
  echo "    [3]  Rapport JSON"
  echo "    [4]  Shell uniquement"
  echo "    [5]  Quitter"
  echo ""
  read -rp "  Votre choix [1-5] : " lsit_choix

  case "$lsit_choix" in
    1)
      echo ""
      echo "  Démarrage du tableau de bord..."
      echo "  --> Ouvre http://localhost:8082 dans ton navigateur."
      echo '  Tapez "exit" ou "end" pour arrêter et revenir ici.'
      echo ""
      lsit --serve
      ;;
    2)
      echo ""
      lsit --format txt
      ;;
    3)
      echo ""
      lsit --format json
      ;;
    4)
      echo ""
      echo "  Commandes disponibles :"
      echo "    lsit --format txt   --> rapport TXT"
      echo "    lsit --format json  --> rapport JSON"
      echo "    lsit --serve        --> tableau de bord web (port 8082)"
      echo ""
      break
      ;;
    5|exit|end)
      echo ""
      exit
      ;;
    *)
      echo "  Choix invalide. Veuillez entrer 1, 2, 3, 4 ou 5."
      ;;
  esac
done
EOF
      chown vagrant:vagrant /home/vagrant/.bash_profile
    SHELL
  end

  # ─── Machine Rocky Linux 9 ───────────────────────────────────────────────────
  config.vm.define "rocky" do |rocky|
    rocky.vm.box = "generic/rocky9"
    rocky.vbguest.auto_update = false
    rocky.vm.network "forwarded_port", guest: 5000, host: 8083

    rocky.vm.synced_folder ".", "/vagrant", type: "rsync",
      rsync__exclude: [".git/", ".vagrant/", "__pycache__/"]

    rocky.vm.provision "shell", inline: <<-SHELL
      # dnf update complet d'abord : installer seulement python3/pip/tree upgrade
      # openssl-libs sans reconstruire openssh-server dans la meme passe, ce qui
      # casse sshd ("OpenSSL version mismatch"). Un update global garde tout coherent.
      dnf update -y
      dnf install -y python3 python3-pip tree
      pip3 install --quiet flask

      # firewalld bloque tout par defaut sauf cockpit/dhcpv6-client/ssh ;
      # sans ca le dashboard Flask (port 5000) est inaccessible depuis l'hote.
      firewall-cmd --permanent --add-port=5000/tcp
      firewall-cmd --reload

      # Supprimer les retours chariot Windows (\r)
      sed -i 's/\r$//' /vagrant/lsit.py \
        /vagrant/Moteur/base/moteur_base.py \
        /vagrant/Moteur/linux/moteur_linux.py \
        /vagrant/Moteur/rocky/moteur_rocky.py

      chmod +x /vagrant/lsit.py
      ln -sf /vagrant/lsit.py /usr/local/bin/lsit
      echo "0 0 * * * root /usr/local/bin/lsit --format json" > /etc/cron.d/lsit_audit

      cat > /etc/profile.d/lsit-welcome.sh << 'EOF'
#!/bin/bash
[[ $- == *i* ]] || return

while true; do
  echo ""
  echo "  ╔══════════════════════════════════════════╗"
  echo "  ║   LSIT - Rocky Linux System Inventory    ║"
  echo "  ╚══════════════════════════════════════════╝"
  echo ""
  echo "    [1]  Interface graphique  (port 8083)"
  echo "    [2]  Rapport TXT"
  echo "    [3]  Rapport JSON"
  echo "    [4]  Shell uniquement"
  echo "    [5]  Quitter"
  echo ""
  read -rp "  Votre choix [1-5] : " lsit_choix

  case "$lsit_choix" in
    1)
      echo ""
      echo "  Démarrage du tableau de bord..."
      echo "  --> Ouvre http://localhost:8083 dans ton navigateur."
      echo '  Tapez "exit" ou "end" pour arrêter et revenir ici.'
      echo ""
      lsit --serve
      ;;
    2)
      echo ""
      lsit --format txt
      ;;
    3)
      echo ""
      lsit --format json
      ;;
    4)
      echo ""
      echo "  Commandes disponibles :"
      echo "    lsit --format txt   --> rapport TXT"
      echo "    lsit --format json  --> rapport JSON"
      echo "    lsit --serve        --> tableau de bord web (port 8083)"
      echo ""
      break
      ;;
    5|exit|end)
      echo ""
      exit
      ;;
    *)
      echo "  Choix invalide. Veuillez entrer 1, 2, 3, 4 ou 5."
      ;;
  esac
done
EOF
      sed -i 's/\r$//' /etc/profile.d/lsit-welcome.sh
      chmod +x /etc/profile.d/lsit-welcome.sh
    SHELL
  end

end
