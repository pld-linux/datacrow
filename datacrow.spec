# TODO
# - bashism: Requires: /bin/bash
# - bundled ix86 binaries: Requires:  libc.so.6 libc.so.6(GLIBC_2.0)

%define	ver	%(echo %{version} | tr . _)
Summary:	Data Crow is a movie, video, book, software, and music cataloguer/database
Name:		datacrow
Version:	3.9.3
Release:	0.3
License:	GPL v3
Group:		X11/Applications
URL:		http://www.datacrow.net/
Source0:	http://downloads.sourceforge.net/datacrow/%{name}_%{ver}_source.zip
# Source0-md5:	48530322114dc028457a31f6699654f2
Source1:	%{name}.sh
Source2:	%{name}.desktop
#BuildRequires:	JTattoo
BuildRequires:	ant
#BuildRequires:	batik
#BuildRequires:	cobra
BuildRequires:	dos2unix
BuildRequires:	fdupes
#BuildRequires:	fop
#BuildRequires:	fop-javadoc
BuildRequires:	jakarta-commons-io
#BuildRequires:	jaudiotagger
BuildRequires:	java-commons-codec
BuildRequires:	java-commons-logging
BuildRequires:	java-cup
#BuildRequires:	java-devel-openjdk
BuildRequires:	java-hsqldb
BuildRequires:	java-log4j
BuildRequires:	java-xalan
#BuildRequires:	java-xerces
BuildRequires:	java-xml-commons
BuildRequires:	jdk >= 1.6
BuildRequires:	jpackage-utils
#BuildRequires:	liquidlnf
#BuildRequires:	metadata-extractor
#BuildRequires:	servletapi5
BuildRequires:	unzip
#BuildRequires:	update-alternatives
#BuildRequires:	xalan-j2-xsltc
#BuildRequires:	xmlbeans
#Requires:	batik
#Requires:	cobra
Requires:	fop
Requires:	jakarta-commons-io
#Requires:	jaudiotagger
Requires:	java-commons-codec
Requires:	java-commons-logging
Requires:	java-hsqldb
Requires:	java-log4j
Requires:	java-xalan
Requires:	java-xerces
Requires:	jpackage-utils
Requires:	jre >= 1.6
#Requires:	laf-plugin
#Requires:	liquidlnf
#Requires:	metadata-extractor
#Requires:	xalan-j2-xsltc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Always wanted to manage all your collections in one product? You want
a product you can customize to your needs? Your search ends here!
Using Data Crow allows you to create a huge database containing all
your collected items.

A lot of work? No! Data Crow retrieves information from the web for
you. Including front covers, screenshots and links to the online
information.

Data Crow is a movie, video, book, software, and music cataloguer
database. It uses freeDB, Amazon, and IMDB Web services. It is highly
customizable, easy to use, and feature rich. It has PDF reporting. It
supports DVDs, audio CDs, and many audio and video file formats.

%package webmodule
Summary:	Webmodule for datacrow
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description webmodule
Webmodule for datacrow.

The web module allows multiple users to connect to one Data Crow
instance remotely at the same time.

%prep
%setup -qc
mv %{name}/* .

%build
export LC_ALL=en_US # source code not US-ASCII
%ant \
	-Dfile.encoding=iso-8859-1

%install
rm -rf $RPM_BUILD_ROOT
# discid
install -d $RPM_BUILD_ROOT%{_bindir}
install -p plugins/discid/linux/discid $RPM_BUILD_ROOT%{_bindir}

# jars
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}
cp -p %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}

# libs
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/lib
cp -p lib/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/lib
for i in chart html jetty laf pdf xml; do
	install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/lib/$i
	cp -p lib/$i/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/lib/$i
done

# plugins
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/plugins
cp -p plugins/*.class $RPM_BUILD_ROOT%{_javadir}/%{name}/plugins

# services, resources, icons, help, ..
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
for i in help icons modules reports resources webapp services upgrade; do
	install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/$i
	cp -a $i $RPM_BUILD_ROOT%{_datadir}/%{name}
done
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/webapp/datacrow/WEB-INF/src
cp -p *.properties $RPM_BUILD_ROOT%{_datadir}/%{name}

# startscript
install -d $RPM_BUILD_ROOT%{_bindir}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}

# icon
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p $RPM_BUILD_ROOT%{_datadir}/%{name}/icons/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}

# menu
install -d $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme/*
%attr(755,root,root) %{_bindir}/datacrow
%attr(755,root,root) %{_bindir}/discid

%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%dir %{_javadir}/%{name}/lib
%{_javadir}/%{name}/lib/*.jar
%{_javadir}/%{name}/lib/html
%dir %{_javadir}/%{name}/lib/pdf
%{_javadir}/%{name}/lib/pdf/*.jar
%dir %{_javadir}/%{name}/lib/xml
%{_javadir}/%{name}/lib/xml/*.jar
%dir %{_javadir}/%{name}/lib/chart
%{_javadir}/%{name}/lib/chart/*.jar
%dir %{_javadir}/%{name}/lib/laf
%{_javadir}/%{name}/lib/laf/*.jar
%dir %{_javadir}/%{name}/plugins
%{_javadir}/%{name}/plugins/*.class

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.properties
%dir %{_datadir}/%{name}/help
%{_datadir}/%{name}/help/*
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/*
%dir %{_datadir}/%{name}/modules
%{_datadir}/%{name}/modules/.*
%{_datadir}/%{name}/modules/*
%dir %{_datadir}/%{name}/reports
%{_datadir}/%{name}/reports/*
%dir %{_datadir}/%{name}/resources
%{_datadir}/%{name}/resources/*.txt
%{_datadir}/%{name}/resources/*.properties
#%dir %{_datadir}/%{name}/themes
#%{_datadir}/%{name}/themes/*.zip
%dir %{_datadir}/%{name}/upgrade
%{_datadir}/%{name}/upgrade/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

# datacrow wants to control services ...
%defattr(664,root,users,775)
%dir %{_datadir}/%{name}/services
%{_datadir}/%{name}/services/*.jar

%files webmodule
%defattr(644,root,root,755)
#%doc readme/webmodule/*.txt
%dir %{_javadir}/%{name}/lib/jetty
%{_javadir}/%{name}/lib/jetty/*.jar
%dir %{_datadir}/%{name}/webapp
%{_datadir}/%{name}/webapp/*
