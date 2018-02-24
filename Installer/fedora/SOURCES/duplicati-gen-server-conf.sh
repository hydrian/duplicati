#!/bin/bash

DEFAULT_SERVER_CONFIG_FILE='/etc/duplicati/server.conf'
DEFAULT_GENERATED_SERVER_CONFIG_FILE='/var/lib/duplicati/server.conf'
DEFAULT_WEBSERVICE_INTERFACE='loopback' 
DEFAULT_WEBSERVICE_PORT='8200'
DEFAULT_WEBSERVICE_PASSWORD=''
DEFAULT_WEBSERVICE_SSLCERTIFICATEFILE='/etc/duplicati/webservice-certificate.pfx'
DEFAULT_LOG_FILE='/var/log/duplicati/server.log'
DEFAULT_LOG_LEVEL='warning'
DEFAULT_LOG_RETENSION='30D'
DEVAULT_SERVER_DATAFOLDER='
DEFAULT_USER='root'
DEFAULT_GROUP='root'
DEFAULTS_FILE='/etc/default/duplicati'


if [ -e "${DEFAULTS_FILE}" ] ; then
	. "${DEFAULTS_FILE}"
else
	echo "Failed to load defaults file ${DEFAULTS_FILE}" 1>&2
	exit 2
fi
 
### Loading conf file 
SERVER_CONFIG_FILE="${SERVER_CONFIG_FILE:-$DEFAULT_SERVER_CONFIG_FILE}"
if [ -e "${SERVER_CONFIG_FILE}" ] ; then
	. "${SERVER_CONFIG_FILE}"
else 
	echo "Failed to find ${SERVER_CONFIG_FILE}" 1>&2
	exit 2
fi

DAEMON_USER="${USER:-$DEFAULT_USER}"
DAEMON_GROUP="${GROUP:-$DEFAULT_GROUP}"

## Generating config file
CONFIG_TMP_FILE=$(mktemp)
GENERATED_SERVER_CONFIG_FILE="${GENERATED_SERVER_CONFIG_FILE:-$DEFAULT_GENERATED_SERVER_CONFIG_FILE}"
echo -- --webservice-interface="${WEBSERVICE_INTERFACE:-$DEFAULT_WEBSERVICE_INTERFACE}" >> "${CONFIG_TMP_FILE}"
echo -- --webservice-port="${WEBSERVICE_PORT:-$DEFAULT_WEBSERVICE_PORT}" >> "${CONFIG_TMP_FILE}"
echo -- --webservice-password="${WEBSERVICE_PASSWORD:-$DEFAULT_WEBSERVICE_PASSWORD}"
if [ ! -z "${WEBSERVICE_SSLCERTIFICATEPASSWORD}" ] ; then 
	if [ -r "${WEBSERVICE_SSLCERTIFICATEFILE}" ] ; then
		echo -- --webservice-sslcertificatepassword="${WEBSERVICE_SSLCERTIFICATEPASSWORD}"
		echo -- --webservice-sslcertificatefile="${WEBSERVICE_SSLCERTIFICATEFILE}}"
	else
		echo "Failed to find and read ${WEBSERVICE_SSLCERTIFICATEFILE}" 1>&2
		exit 2
	fi
fi  

echo -- --log-file="${LOG_FILE:-DEFAULT_LOG_FILE}" >> "${CONFIG_TMP_FILE}"
echo -- --log-level="${LOG_LEVEL,,:-$DEFAULT_LOG_LEVEL}" >> "${CONFIG_TMP_FILE}"
echo -- --log-retention="${LOG_RETENTION:-$DEFAULT_LOG_RETENTION}"
if [ ! -z "${SERVER_ENCRYPTION_KEY}" ] ; then
	echo -- --server-encryption-key="${SERVER_ENCRYPTION_KEY}" >> "${CONFIG_TMP_FILE}"
else
	echo -- --unencrypted-database >> "${CONFIG_TMP_FILE}"
fi

cp "${CONFIG_TMP_FILE}" "${GENERATED_SERVER_CONFIG_FILE}"
if [ ! eq 0 ] ; then
	echo "Failed to update generated config file ${GENERATED_SERVER_CONFIG_FILE}" 1>&2
	exit 2
fi
chown "${DAEMON_USER}":"${DAEMON_GROUP}" "${GENERATED_SERVER_CONFIG_FILE}"
chmod 600 "${GENERATED_SERVER_CONFIG_FILE}"
rm "${CONFIG_TMP_FILE}" 
exit 0 