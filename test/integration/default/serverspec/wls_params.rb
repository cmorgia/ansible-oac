# -*- mode: ruby -*-
# vi: set ft=ruby :

ORACLE_BASE_DIR="/u01/app/oracle"
ORACLE_MIDDLEWARE_DIR="#{ORACLE_BASE_DIR}/product/middleware"
OAC_HOME_DIR="#{ORACLE_MIDDLEWARE_DIR}/oac"
WEBLOGIC_DOMAIN_HOME="#{ORACLE_MIDDLEWARE_DIR}/user_projects/domains/oac_domain"
WEBLOGIC_NODEMANAGER_HOME="#{ORACLE_MIDDLEWARE_DIR}/user_projects/nodemanagers/oac_domain"
WEBLOGIC_ADMIN_SERVER_HOME="#{WEBLOGIC_DOMAIN_HOME}/servers/AdminServer"
WEBLOGIC_MANAGED_SERVER_HOME="#{WEBLOGIC_DOMAIN_HOME}/servers/OAC_Server_1"
