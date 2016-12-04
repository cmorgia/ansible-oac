#
# This is a WLST script to create and configure an OAC cluster.
#

print '[INFO] Setting parameters..'
machines=cluster_nodes.split(",")
server_groups=['OER-MGD-SVRS']
data_source_driver='oracle.jdbc.OracleDriver'
data_source_test='SQL SELECT 1 FROM DUAL'

domain_application_home = os.getenv('DOMAIN_APPLICATION_HOME')
domain_configuration_home = os.getenv('DOMAIN_CONFIGURATION_HOME')
fusion_middleware_home = os.getenv('FUSION_MIDDLEWARE_HOME')
middleware_home = os.getenv('MIDDLEWARE_HOME')
nodemanager_home = os.getenv('NODE_MANAGER_HOME')
weblogic_home = os.getenv('WEBLOGIC_HOME')

weblogic_template = middleware_home + '/wlserver/common/templates/wls/wls.jar'
oac_template = middleware_home + '/oer/common/templates/wls/oracle.oer.oac_server_wls_template_12.1.3.jar'

print "[INFO] Create domain '%s' " % domain_name
readTemplate(weblogic_template)
setOption('AppDir', domain_application_home)
setOption('DomainName', domain_name)
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode', 'prod')
setOption('NodeManagerType', 'CustomLocationNodeManager')
setOption('NodeManagerHome', nodemanager_home)
cd('/Security/base_domain/User/weblogic')
cmo.setName(admin_username)
cmo.setUserPassword(admin_password)
cd('/')

print '[INFO] Save domain'
writeDomain(domain_configuration_home)
closeTemplate()

print '[INFO] Read domain'
readDomain(domain_configuration_home)

print '[INFO] Add OAC tempalte..'
addTemplate(oac_template)

print "[INFO] Retarget JMS resources.."
filestores = cmo.getFileStores()
for filestore in filestores:
    filestore.setDirectory(domain_application_home)
    targets = filestore.getTargets()
    for target in targets:
        if ' (migratable)' in target.getName():
            assign('FileStore', filestore.getName(), 'Target', target.getName().strip(' (migratable)'))
jmsservers = cmo.getJMSServers()
for jmsserver in jmsservers:
    targets = jmsserver.getTargets()
    for target in targets:
        if ' (migratable)' in target.getName():
            assign('JMSServer', jmsserver.getName(), 'Target', target.getName().strip(' (migratable)'))
safagents = cmo.getSAFAgents()
for safagent in safagents:
    targets = safagent.getTargets()
    for target in targets:
        if ' (migratable)' in target.getName():
            assign('SAFAgent', safagent.getName(), 'Target', target.getName().strip(' (migratable)'))

print '[INFO] Adjust data source settings..'
jdbcsystemresources = cmo.getJDBCSystemResources()
for jdbcsystemresource in jdbcsystemresources:
    cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' \
        + jdbcsystemresource.getName() + '/JDBCConnectionPoolParams/NO_NAME_0')
    cmo.setInitialCapacity(1)
    cmo.setMaxCapacity(15)
    cmo.setMinCapacity(1)
    cmo.setStatementCacheSize(0)
    cmo.setTestConnectionsOnReserve(java.lang.Boolean('false'))
    cmo.setTestTableName(data_source_test)
    cmo.setConnectionCreationRetryFrequencySeconds(30)
    cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' \
        + jdbcsystemresource.getName() + '/JDBCDriverParams/NO_NAME_0')
    cmo.setUrl(data_source_url)
    cmo.setPasswordEncrypted(data_source_password)
    cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' \
        + jdbcsystemresource.getName() + '/JDBCDriverParams/NO_NAME_0/Properties/NO_NAME_0/Property/user')
    cmo.setValue(cmo.getValue().replace('DEV', data_source_user_prefix))
    cd('/')

print '[INFO] Set NodeManager credentials'
cd('/SecurityConfiguration/' + domain_name)
cmo.setNodeManagerUsername(nodemanager_username)
cmo.setNodeManagerPasswordEncrypted(nodemanager_password)

print '[INFO] Configuring AdminServer..'
cd('/Server/' + admin_server_name)
cmo.setListenAddress(admin_server_listen_address)
cmo.setListenPort(int(admin_server_listen_port))
create(admin_server_name,'SSL')
cd('SSL/' + admin_server_name)
cmo.setHostnameVerificationIgnored(true)
cmo.setHostnameVerifier(None)
cmo.setTwoWaySSLEnabled(false)
cmo.setClientCertificateEnforced(false)

print '[INFO] Set up authentication configuration'
cd('/SecurityConfiguration/'+ domain_name +'/Realms/myrealm')
cd('AuthenticationProviders/DefaultAuthenticator')
set('ControlFlag', 'SUFFICIENT')
cd('../../')

print '[INFO] Save changes'
updateDomain()
closeDomain()
