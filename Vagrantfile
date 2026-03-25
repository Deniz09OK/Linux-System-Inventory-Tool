Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.vbguest.auto_update = false
  config.vm.network "forwarded_port", guest: 8080, host: 8081

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip nano tree

    chmod +x /vagrant/lsit.py
    ln -sf /vagrant/lsit.py /usr/local/bin/lsit

    echo "0 0 * * * root /usr/local/bin/lsit --format json" > /etc/cron.d/lsit_audit

    cat > /etc/profile.d/lsit-welcome.sh << 'EOF'
#!/bin/bash
[[ $- == *i* ]] || return

while true; do
  echo ""
  echo "  ╔══════════════════════════════════════════╗"
  echo "  ║   LSIT - Linux System Inventory Tool    ║"
  echo "  ╚══════════════════════════════════════════╝"
  echo ""
  echo "    [1]  Interface graphique  (port 8081)"
  echo "    [2]  Ligne de commande    (rapport TXT/JSON)"
  echo "    [3]  Shell uniquement"
  echo "    [4]  Quitter"
  echo ""
  read -rp "  Votre choix [1-4] : " lsit_choix

  case "$lsit_choix" in
    1)
      echo ""
      echo "  Démarrage du tableau de bord..."
      echo "  --> Ouvre http://localhost:8081 dans ton navigateur."
      echo '  Tapez "exit" ou "end" pour arrêter et revenir ici.'
      echo ""
      python3 /vagrant/lsit.py --serve
      ;;
    2)
      echo ""
      lsit
      ;;
    3)
      echo ""
      echo "  Commandes disponibles :"
      echo "    lsit                --> rapport TXT"
      echo "    lsit --format json  --> rapport JSON"
      echo "    lsit --serve        --> tableau de bord web (port 8081)"
      echo ""
      break
      ;;
    4|exit|end)
      echo ""
      exit
      ;;
    *)
      echo "  Choix invalide. Veuillez entrer 1, 2, 3 ou 4."
      ;;
  esac
done
EOF
    chmod +x /etc/profile.d/lsit-welcome.sh
  SHELL
end