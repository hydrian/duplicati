# TODO:
# - check where Tools/* scripts should really be
# - try to fix every mono compiler warning
# - fix rpmlint warnings

# Set up some defaults

%global debug_package %{nil}
%global alphatag .git

# Then load overrides
# %include "%{_topdir}/SOURCES/%{name}-buildinfo.spec"

Name:      duplicati
Version:  2.0.0
Release:  %{_buildtag}
#BuildArch:  noarch

# Disable auto dependencies as it picks up .Net 2.0 profile
#   and does not support supplying them with 4.5
# Also, all thirdparty libraries are given as "provides" but they
#   are not installed for use externally
AutoReqProv: no
#Group:      System Environments/Libraries
Summary:  Backup client for encrypted online backups
License:  LGPLv2+
URL:  http://www.duplicati.com
Source0:  duplicati-%{_buildversion}.tar.bz2
Source1:  %{name}-make-binary-package.sh
Source2:  %{name}-install-recursive.sh
Source3:  %{name}.service
Source4:  %{name}.default
Source5:  %{name}.upstart
Source6:  %{name}-gen-server-conf.sh
Source7:  server.conf

BuildRequires: mono
BuildRequires: mono-addins-devel
BuildRequires: nuget

Requires:  bash
Requires:  sqlite >= 3.6.12
%if 0%{?centos} 
Requires:   epel-release
%endif
Requires:  mono-core >= 3.0
Requires:  mono-data-sqlite
Requires:  mono(System)
Requires:  mono(System.Configuration)
Requires:  mono(System.Configuration.Install)
Requires:  mono(System.Core)
Requires:  mono(System.Data)
Requires:  mono(System.Drawing)
Requires:  mono(System.Net)
Requires:  mono(System.Net.Http)
Requires:  mono(System.Net.Http.WebRequest)
Requires:  mono(System.Runtime.Serialization)
Requires:  mono(System.ServiceModel)
Requires:  mono(System.ServiceModel.Discovery)
Requires:  mono(System.ServiceProcess)
Requires:  mono(System.Transactions)
Requires:  mono(System.Web)
Requires:  mono(System.Web.Services)
Requires:  mono(System.Xml)
Requires:  mono(System.Xml.Linq)
Requires:  mono(Mono.Security)
Requires:  mono(Mono.Posix)
Requires:  gnupg

Provides:  duplicati = %{version}
Provides:  duplicati-cli = %{version}
Obsoletes: %{name} <= %{version}

%package server
Summary:  Server components to Duplicati
#Group:    System Environments/Daemons
Requires:  %{name} = %{version}
Requires:  systemd
Provides:  duplicati-server = %{version}
Obsoletes: %{name} <= %{version}

%package gui
Summary:   GUI for Duplicati and user level application 
#Group:    Applications/Archiving
Requires:  %{name} = %{version}
Requires:  desktop-file-utils
Requires:  mono(appindicator-sharp)
Requires:  libappindicator
Requires:  gtk-update-icon-cache
Requires:  libdbusmenu-gtk2
Provides:  duplicati-gui = %{version}
Obsoletes: %{name} <= %{version}
Icon:      duplicati.xpm

%description 
Duplicati is a free backup client that securely stores encrypted,
incremental, compressed backups on cloud storage services and remote file
servers.  It supports targets like Amazon S3, Windows Live SkyDrive,
Rackspace Cloud Files or WebDAV, SSH, FTP (and many more).
 
Duplicati has built-in AES-256 encryption and backups be can signed using
GNU Privacy Guard.  A built-in scheduler makes sure that backups are always
up-to-date.  Last but not least, Duplicati provides various options and
tweaks like filters, deletion rules, transfer and bandwidth options to run
backups for specific purposes.

%description server
Duplicati is a free backup client that securely stores encrypted,
incremental, compressed backups on cloud storage services and remote file
servers.  It supports targets like Amazon S3, Windows Live SkyDrive,
Rackspace Cloud Files or WebDAV, SSH, FTP (and many more).
 
Duplicati has built-in AES-256 encryption and backups be can signed using
GNU Privacy Guard.  A built-in scheduler makes sure that backups are always
up-to-date.  Last but not least, Duplicati provides various options and
tweaks like filters, deletion rules, transfer and bandwidth options to run
backups for specific purposes.

Contains server components

%description gui
Duplicati is a free backup client that securely stores encrypted,
incremental, compressed backups on cloud storage services and remote file
servers.  It supports targets like Amazon S3, Windows Live SkyDrive,
Rackspace Cloud Files or WebDAV, SSH, FTP (and many more).
 
Duplicati has built-in AES-256 encryption and backups be can signed using
GNU Privacy Guard.  A built-in scheduler makes sure that backups are always
up-to-date.  Last but not least, Duplsicati provides various options and
tweaks like filters, deletion rules, transfer and bandwidth options to run
backups for specific purposes.

Contains desktop GUI components

%prep
%setup -q -n %{name}-%{_buildversion}

%build

# removing non-platform thirdparty binaries:
rm -rf win-tools
rm -rf SQLite/win64
rm -rf SQLite/win32
rm -rf MonoMac.dll
rm -rf alphavss
rm -rf OSX\ Icons
rm -rf OSXTrayHost
rm AlphaFS.dll
rm AlphaVSS.Common.dll
rm -rf licenses/alphavss
rm -rf licenses/MonoMac
rm -rf licenses/gpg
find . -iname \*.bat --delete


%install

# Mono binaries are installed in /usr/lib, not /usr/lib64, even on x86_64:
# https://fedoraproject.org/wiki/Packaging:Mono

install -d %{buildroot}%{_datadir}/pixmaps/
install -d %{buildroot}%{_lib}/%{name}/
install -d %{buildroot}%{_lib}/%{name}/SVGIcons/
install -d %{buildroot}%{_lib}/%{name}/SVGIcons/dark/
install -d %{buildroot}%{_lib}/%{name}/SVGIcons/light/
install -d %{buildroot}%{_lib}/%{name}/licenses/
install -d %{buildroot}%{_lib}/%{name}/webroot/
install -d %{buildroot}%{_lib}/%{name}/lvm-scripts/

/bin/bash %{_topdir}/SOURCES/%{name}-install-recursive.sh "." "%{buildroot}%{_exec_prefix}/lib/%{name}/"

# We do not want these files in the lib folder
rm "%{buildroot}%{_lib}/%{name}/%{name}-launcher.sh"
rm "%{buildroot}%{_lib}/%{name}/%{name}-commandline-launcher.sh"
rm "%{buildroot}%{_lib}/%{name}/%{name}-server-launcher.sh"
rm "%{buildroot}%{_lib}/%{name}/%{name}.png"
rm "%{buildroot}%{_lib}/%{name}/%{name}.desktop"
rm "%{buildroot}%{_lib}/Duplicati.WindowsService.exe"*

# Then we install them in the correct spots
install -p -D -m 755 %{name}-launcher.sh %{buildroot}%{_bindir}/%{name}
install -p -D -m 755 %{name}-commandline-launcher.sh %{buildroot}%{_bindir}/%{name}-cli
install -p -D -m 755 %{name}-server-launcher.sh %{buildroot}%{_bindir}/%{name}-server
install -p  %{name}.png %{buildroot}%{_datadir}/pixmaps/

desktop-file-install %{name}.desktop

# Install the service:

%if 0%{rhel} > 6
# rhel/centos - systemd
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_unitdir}
%elseif 0%{fedora} > 24
#fedora core - systemd 
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_unitdir}
%else
#fall back to Upstart  
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initdir}/%{name}
%endif

install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Create data directory
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# Creating configuration directory
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

%clean
%if "%{noclean}" == ""
   rm -rf $RPM_BUILD_ROOT
%endif


%post server
%if 0%{rhel} > 6
# rhel/centos - systemd
%systemd_post %{name}.services
%elseif 0%{fedora} > 24
#fedora core - systemd
%systemd_post %{name}.services 
%else
#fall back to Upstart  
chkconfig --enable %{name}
%endif

%preun server
%if 0%{rhel} > 6
# rhel/centos - systemd
%systemd_preun %{name}.service
%elseif 0%{fedora} > 24
#fedora core - systemd
%systemd_preun %{name}.service
%else
#fall back to Upstart  
service %{name} stop
chkconfig --disable %{name}
%endif


%postun server
%if 0%{rhel} > 6
# rhel/centos - systemd
%systemd_postun_with_restart %{name}.service
%elseif 0%{fedora} > 24
#fedora core - systemd
%systemd_postun_with_restart %{name}.service
%endif


%post gui
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor 2> /dev/null

%postun gui
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor 2> /dev/null

%posttrans gui
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null 


%files
%defattr(0640, root, root, 750)
%doc changelog.txt licenses/license.txt
%{_bindir}/%{name}-cli
%{_datadir}/*/*
%{_libdir/${name}/%{name}.CommandLine.*
%{_libdir/${name}/%{name}.Library.*
%{_libdir/${name}/%{name}.License.*
%{_libdir/${name}/*.dll

%files server
%defattr(0640, root, root, 750)
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %attr(0700,root,root) %{_sysconfdir}/%{name}/server.conf
%doc %{_sysconfdir}/%{name}/server.conf.example
%attr(0700,root,root) %{_sharedstatedir}/%{name}
%{_libdir}/%{name}/Duplicati.Server.*
%{_bindir}/%{name}-server
%if 0%{rhel} > 6
# Centos/RHEL 7 or greater
%{_unitdir}/*
%endif
# Supported version that uses SystemD
%elseif 0%{fedora} > 24
%{_unitdir}/*
%else
#Uses Upstart
%{_sysconfdir}/*
%if

%files gui
%defattr(0640, root, root, 750)
%{_libdir}/%{_name}/Duplicati.GUI.*
%{_libdir}/%{_name}/Duplicati.Library.AutoUpdater.*
%{_bindir}/%{_name}
%{_datadir}/pixmaps/*

%changelog
* Wed Jun 21 2017 Kenneth Skovhede <kenneth@duplicati.com> - 2.0.0-0.20170621.git
- Added the service file to the install

* Thu Apr 28 2016 Kenneth Skovhede <kenneth@duplicati.com> - 2.0.0-0.20160423.git
- Made a binary version of the spec file

* Sat Apr 23 2016 Kenneth Skovhede <kenneth@duplicati.com> - 2.0.0-0.20160423.git
- Updated list of dependencies

* Thu Mar 27 2014 Kenneth Skovhede <kenneth@duplicati.com> - 2.0.0-0.20140326.git
- Moved to /usr/lib
- Fixed minor build issues

* Wed Mar 26 2014 Kenneth Skovhede <kenneth@duplicati.com> - 2.0.0-0.20140326.git
- Updated patch files
- Fixed minor build issues

* Wed May 29 2013 Ismael Olea <ismael@olea.org> - 2.0.0-0.20130529.git
- removed MacOSX support and deps
- first compiler building spec

* Mon May 13 2013 Ismael Olea <ismael@olea.org> - 1.3.4-1
- removing desktop contents

* Sun May 12 2013 Ismael Olea <ismael@olea.org> - 1.3.4-0
- first dirty package for upstream compiled binary


