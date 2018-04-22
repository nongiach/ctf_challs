export PATH="$PATH:/opt/bin:/opt/sbin"

cd /root
which opkg ||
  (sh install_pkg_manager.sh &&
  opkg install ncat &&
  poweroff -f)
echo 0 > /proc/sys/kernel/randomize_va_space
echo | adduser lamer
chmod 000 *
chmod +rx ./vuln .
chmod +r flag
ncat -k -l -p 4242 -c "su lamer -c ./vuln"
