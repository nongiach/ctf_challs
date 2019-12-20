set -e
sh clean.sh
generate_keys() {
  if [ ! "$#" -gt 0 ]; then echo "ERROR Usage: server or client"; exit ; fi
  FILENAME=$1
  # openssl genrsa -out $FILENAME.key 1024 
  openssl genrsa -out $FILENAME.key 2048
  openssl req -new -key $FILENAME.key -x509 -days 3653 -out $FILENAME.crt -batch
  cat $FILENAME.key $FILENAME.crt >$FILENAME.pem
  chmod 600 $FILENAME.key $FILENAME.pem 
  rm $FILENAME.key
}

generate_keys server
generate_keys client
