%define           hhvm_dir %{_var}/hhvm
%define           hhvm_group hhvm
%define           hhvm_user hhvm
%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm
Version:          3.3.0
Release:          1%{?dist}
Summary:          HipHop VM (HHVM) is a virtual machine for executing programs written in PHP

Group:            Development/Compiler
License:          PHP/Zend
URL:              http://hhvm.com
Source0:          https://github.com/facebook/hhvm/archive/%{name}-%{version}.tar.gz
Source1:          server.hdf
Source2:          config.hdf
Source3:          hhvm.service
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, libevent-devel >= 2.0
BuildRequires:    libcurl-devel >= 7.29
BuildRequires:    glog-devel >= 0.3.3, jemalloc-devel >= 3.6, tbb-devel >= 4.1
BuildRequires:    libmcrypt-devel >= 2.5.8, libdwarf-devel >= 20130207
BuildRequires:    libxml2-devel libicu-devel
BuildRequires:    oniguruma-devel readline-devel
#BuildRequires:   libc-client-devel pam-devel gd-devel
BuildRequires:    libcap-devel libedit-devel pcre-devel sqlite-devel
BuildRequires:    inotify-tools-devel lz4-devel >= r121-2
BuildRequires:    boost-devel >= 1.48, libmemcached-devel >= 0.39
BuildRequires:    mysql-devel, libxslt-devel, expat-devel, bzip2-devel, openldap-devel
BuildRequires:    elfutils-libelf-devel, binutils-devel, libevent-devel, ImageMagick-devel
BuildRequires:    libvpx-devel, libpng-devel, gmp-devel, ocaml

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Requires:         systemd
Requires:         glog >= 0.3.3, jemalloc >= 3.0, tbb >= 4.0
Requires:         libmcrypt >= 2.5.8, libdwarf >= 20130207
Requires:         boost >= 1.50, libmemcached >= 0.39, lz4 >= r121-2
Requires:         libxml2, libicu
Requires:         oniguruma, readline, pam, libcap, libedit, pcre, sqlite, libxslt,
Requires:         expat, bzip2, openldap, elfutils-libelf, binutils, libevent, ImageMagick,
Requires:         libvpx, libpng, gmp, ocaml

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for executing
programs written in PHP.
HHVM uses a just-in-time compilation approach to achieve superior performance
while maintaining the flexibility that PHP developers are accustomed to.
HipHop VM (and before it HPHPc) has realized > 5x increase in throughput for
Facebook compared with Zend PHP 5.2.

HipHop is most commonly run as a standalone server, replacing both Apache and
modphp.

%package          devel
Summary:          Library links and header files for HHVM development
Group:            Development/Libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, libevent-devel >= 2.0
BuildRequires:    libcurl-devel >= 7.29
BuildRequires:    glog-devel >= 0.3.3, jemalloc-devel >= 3.6, tbb-devel >= 4.1
BuildRequires:    libmcrypt-devel >= 2.5.8, libdwarf-devel >= 20130207
BuildRequires:    libxml2-devel libicu-devel
BuildRequires:    oniguruma-devel readline-devel
BuildRequires:    libcap-devel libedit-devel pcre-devel sqlite-devel
BuildRequires:    inotify-tools-devel lz4-devel >= r121-2
BuildRequires:    boost-devel >= 1.48, libmemcached-devel >= 0.39
BuildRequires:    mysql-devel libxslt-devel expat-devel bzip2-devel openldap-devel
BuildRequires:    elfutils-libelf-devel binutils-devel libevent-devel ImageMagick-devel
BuildRequires:    libvpx-devel libpng-devel gmp-devel ocaml
Provides:         hhvm-devel = %{version}-%{release}

%description devel
hhvm-devel contains the library links and header files you'll
need to develop HHVM applications.

%prep
%setup -q -n %{name}-%{version}

%build
export HPHP_HOME=`pwd`
export CPLUS_INCLUDE_PATH=/usr/include/libdwarf
git submodule update --init --recursive
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DLIBEVENT_LIB=/usr/lib64/libevent.so \
    -DLIBEVENT_INCLUDE_DIR=/usr/include \
    -DLIBINOTIFY_LIBRARY=/usr/lib64/libinotifytools.so.0 .
make %{?_smp_mflags}

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
# Create default directory
# TODO: store pid and similar files in /run/hhvm/ instead of /var/run/hhvm
# https://fedoraproject.org/wiki/Packaging:Tmpfiles.d
%{__mkdir} -p %{buildroot}%{_var}/run/%{name}
%{__mkdir} -p %{buildroot}%{_var}/log/%{name}
%{__mkdir} -p %{buildroot}%{_var}/hhvm

%{__install} -p -D -m 0755 hphp/hhvm/hhvm %{buildroot}%{_bindir}/hhvm
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize %{buildroot}%{_bindir}/hphpize
%{__install} -p -D -m 0755 hphp/hack/bin/hh_client %{buildroot}%{_bindir}/hh_client
%{__install} -p -D -m 0755 hphp/hack/bin/hh_client %{buildroot}%{_bindir}/hh_server

# Install hhvm and systemctl configuration
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/hhvm/server.hdf
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/hhvm/config.hdf
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/hhvm.service

#devel
%{__mkdir} -p %{buildroot}/usr/local/lib64/hhvm/CMake
%{__mkdir} -p %{buildroot}/usr/local/lib
%{__mkdir} -p %{buildroot}/usr/local/bin
%{__mkdir} -p %{buildroot}/usr/local/include
%{__mkdir} -p %{buildroot}/usr/local/man/man3
%{__mkdir} -p %{buildroot}/usr/local/share/doc/pcre/html

#header files
%{__install} -p -D -m 0755 CMake/*.cmake %{buildroot}/usr/local/lib64/hhvm/CMake
%{__install} -p -D -m 0755 third-party/pcre/libpcre.a %{buildroot}/usr/local/lib/libpcre.a
%{__install} -p -D -m 0755 third-party/pcre/libpcreposix.a %{buildroot}/usr/local/lib/libpcreposix.a
%{__install} -p -D -m 0755 third-party/pcre/libpcrecpp.a %{buildroot}/usr/local/lib/libpcrecpp.a
%{__install} -p -D -m 0755 third-party/pcre/pcregrep %{buildroot}/usr/local/bin/pcregrep
%{__install} -p -D -m 0755 third-party/pcre/pcretest %{buildroot}/usr/local/bin/pcretest
%{__install} -p -D -m 0755 third-party/pcre/pcrecpp_unittest %{buildroot}/usr/local/bin/pcrecpp_unittest
%{__install} -p -D -m 0755 third-party/pcre/pcre_scanner_unittest %{buildroot}/usr/local/bin/pcre_scanner_unittest
%{__install} -p -D -m 0755 third-party/pcre/pcre_stringpiece_unittest %{buildroot}/usr/local/bin/pcre_stringpiece_unittest
%{__install} -p -D -m 0755 third-party/pcre/pcre.h %{buildroot}/usr/local/include/pcre.h
%{__install} -p -D -m 0755 third-party/pcre/pcreposix.h %{buildroot}/usr/local/include/pcreposix.h
%{__install} -p -D -m 0755 third-party/pcre/pcrecpp.h %{buildroot}/usr/local/include/pcrecpp.h
%{__install} -p -D -m 0755 third-party/pcre/pcre_scanner.h %{buildroot}/usr/local/include/pcre_scanner.h
%{__install} -p -D -m 0755 third-party/pcre/pcrecpparg.h %{buildroot}/usr/local/include/pcrecpparg.h
%{__install} -p -D -m 0755 third-party/pcre/pcre_stringpiece.h %{buildroot}/usr/local/include/pcre_stringpiece.h

#man pages
%{__install} -p -D -m 0755 third-party/pcre/doc/*.3 %{buildroot}/usr/local/man/man3
%{__install} -p -D -m 0755 third-party/pcre/doc/html/*.html %{buildroot}/usr/local/share/doc/pcre/html

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{hhvm_group} >/dev/null || groupadd -r %{hhvm_group}
getent passwd %{hhvm_user} >/dev/null || \
    useradd -r -g %{hhvm_group} -d %{hhvm_dir} -s /sbin/nologin \
    -c "HHVM" %{hhvm_user}
exit 0

%post -p /sbin/ldconfig
%systemd_post hhvm.service

%systemd_preun hhvm.service

%postun -p /sbin/ldconfig
%systemd_postun hhvm.service

%files
%defattr(-,hhvm,hhvm,-)
%{_unitdir}/hhvm.service
%dir %{_var}/hhvm
%dir %{_var}/run/%{name}
%dir %{_var}/log/%{name}

%defattr(-,root,root,-)
%dir %{_sysconfdir}/hhvm
%config(noreplace) %{_sysconfdir}/hhvm/server.hdf
%config(noreplace) %{_sysconfdir}/hhvm/config.hdf
%{_bindir}/hhvm
%{_bindir}/hphpize
%{_bindir}/hh_client
%{_bindir}/hh_server

%files devel
%defattr(-,root,root,-)
/usr/local/lib64/hhvm/CMake/*.cmake
/usr/local/lib/libpcre.a
/usr/local/lib/libpcreposix.a
/usr/local/lib/libpcrecpp.a
/usr/local/bin/pcregrep
/usr/local/bin/pcretest
/usr/local/bin/pcrecpp_unittest
/usr/local/bin/pcre_scanner_unittest
/usr/local/bin/pcre_stringpiece_unittest
/usr/local/include/pcre.h
/usr/local/include/pcreposix.h
/usr/local/include/pcrecpp.h
/usr/local/include/pcre_scanner.h
/usr/local/include/pcrecpparg.h
/usr/local/include/pcre_stringpiece.h
/usr/local/man/man3/*
/usr/local/share/doc/pcre/html/*

%doc CONTRIBUTING.md LICENSE.PHP LICENSE.ZEND README.md hphp/NEWS

%changelog

* Fri Sep 19 2014 Paul Moss <no1youknowz@gmail.com> - 3.3
- Initial built for el7
