#!/bin/sh
set +e

for i in `seq $TIMEOUT` ; do
  nc -z "$DB_HOST" "$DB_PORT" > /dev/null 2>&1

  result=$?
  if [ $result -eq 0 ] ; then
    if [ $# -gt 0 ] ; then
      /migrate-orig -path=/migrations/ -database postgres://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME?sslmode=disable $@
    fi
    exit 0
  fi
  sleep 1
done
echo "Operation timed out" >&2
exit 1
