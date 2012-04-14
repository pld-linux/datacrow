#!/bin/bash
#
# startscript for datacrow
#
# written by oc2pus
#
# Changelog:
# 18.10.2006 initial version
# 25.01.2007 added packman packages: metadata-extractor hsqldb
# 05.04.2007 added xalan-j2, xerces-j2 splittet CLASSPATH
#            new reports subdir
# 27.10.2007 renamed helpfiles ==> help
#            added subdir modules and upgrades
# 22.01.2008 added log4j
#            added *.properties
#            new main-class
# 25.03.2008 added plugin subdir
# 13.06.2008 added webapp subdir
# 03.09.2008 removed entagged-*
# 02.11.2008 added BrowserLauncher2 and jaudiotagger
# 20.12.2008 added xsltc and JTattoo
# 25.01.2009 readded jaudiotagger
# 24.11.2009 changed createLocalDir to reflect actual layout and use ln -sf
# 04.12.2009 removed themes and skinlf

# activate for debugging
#set -x

# base settings
# home-directory of datacrow
myDataCrowHome=/usr/share/datacrow

# creates a local working directory in user-home
function createLocalDir ()
{
	if [ ! -d $HOME/.datacrow ]; then
		echo "creating local working directory $HOME/.datacrow ..."
		mkdir -p $HOME/.datacrow
	fi

	# a link doesn't work ...
	cp /usr/share/java/datacrow/datacrow.jar $HOME/.datacrow
	ln -sf /usr/share/java/datacrow/lib      $HOME/.datacrow

	ln -sf $myDataCrowHome/help      $HOME/.datacrow
	ln -sf $myDataCrowHome/icons     $HOME/.datacrow
	ln -sf $myDataCrowHome/resources $HOME/.datacrow
#	ln -sf $myDataCrowHome/themes    $HOME/.datacrow

	# new in 3.x
	if [ ! -d $HOME/.datacrow/modules ]; then
		mkdir -p $HOME/.datacrow/modules
		cp -r $myDataCrowHome/modules $HOME/.datacrow
	fi
	ln -sf $myDataCrowHome/upgrade $HOME/.datacrow
	if [ ! -f $HOME/.datacrow/log4j.properties ]; then
		cp $myDataCrowHome/log4j.properties $HOME/.datacrow
	fi

	# new in 3.2
	mkdir -p $HOME/.datacrow/plugins
	ln -sf /usr/share/java/datacrow/plugins/*.class $HOME/.datacrow/plugins

	# new in 3.3
	webmodule=`LANG=C rpm -q datacrow-webmodule`
	if [ "$webmodule" == "package datacrow-webmodule is not installed" ]; then
		rm -rf $HOME/.datacrow/webapp
	else
		rm -rf $HOME/.datacrow/webapp
		cp -r $myDataCrowHome/webapp $HOME/.datacrow
	fi

	# new in 3.9.2
	if [ ! -d $HOME/.datacrow/services ]; then
		mkdir -p $HOME/.datacrow/services
	cp -r $myDataCrowHome/services $HOME/.datacrow
	fi
	if [ ! -d $HOME/.datacrow/reports ]; then
		mkdir -p $HOME/.datacrow/reports
	cp -r $myDataCrowHome/reports   $HOME/.datacrow
	fi
}

echo ""
echo "starting datacrow ..."

# creates a local working directory in user-home
createLocalDir

# change to the working directory
echo "changing to local working directory ~/.datacrow ..."
cd $HOME/.datacrow

# source the jpackage helpers
VERBOSE=1
. /usr/share/java-utils/java-functions

# set JAVA_* environment variables
set_javacmd
check_java_env
set_jvm_dirs

set_flags "-Xmx1024m"

CLASSPATH1=./datacrow.jar:./help/
CLASSPATH2=`build-classpath hsqldb jaudiotagger JTattoo laf-plugin liquidlnf metadata-extractor`
CLASSPATH3=`build-classpath jakarta-commons-logging log4j xalan-j2 xalan-j2-serializer xerces-j2 xsltc`
CLASSPATH4=`build-classpath datacrow`
CLASSPATH=$CLASSPATH1:$CLASSPATH2:$CLASSPATH3:$CLASSPATH4
MAIN_CLASS="net.datacrow.core.DataCrow"

echo "launching datacrow ..."
run -dir:$HOME/.datacrow "$@"
echo "exiting datacrow ..."
