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
Source4:          php.ini
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, libevent-devel >= 2.0
BuildRequires:    glog-devel >= 0.3.3, jemalloc-devel >= 3.6, tbb-devel >= 4.1
BuildRequires:    libmcrypt-devel >= 2.5.8, libdwarf-devel >= 20130207
BuildRequires:    libxml2-devel, libicu-devel, libcurl-devel >= 7.29
BuildRequires:    oniguruma-devel, readline-devel, double-conversion-devel
#BuildRequires:   libc-client-devel, pam-devel, gd-devel
BuildRequires:    libcap-devel, libedit-devel, pcre-devel, sqlite-devel
BuildRequires:    inotify-tools-devel, lz4-devel >= r121-2
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
Requires:         libxml2, libicu, oniguruma, readline, pam, libcap, libedit, pcre, sqlite
Requires:         libxslt, double-conversion, expat, bzip2, openldap, elfutils-libelf
Requires:         binutils, libevent, ImageMagick, libvpx, libpng, gmp, ocaml, libyaml, libzip

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for executing
programs written in PHP.
HHVM uses a just-in-time compilation approach to achieve superior performance
while maintaining the flexibility that PHP developers are accustomed to.

%package          devel
Summary:          Library links and header files for HHVM development
Group:            Development/Libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, libevent-devel >= 2.0
BuildRequires:    libcurl-devel >= 7.29, double-conversion-devel
BuildRequires:    glog-devel >= 0.3.3, jemalloc-devel >= 3.6, tbb-devel >= 4.1
BuildRequires:    libmcrypt-devel >= 2.5.8, libdwarf-devel >= 20130207
BuildRequires:    libxml2-devel, libicu-devel, oniguruma-devel, readline-devel
BuildRequires:    libcap-devel, libedit-devel, pcre-devel, sqlite-devel
BuildRequires:    inotify-tools-devel, lz4-devel >= r121-2
BuildRequires:    boost-devel >= 1.48, libmemcached-devel >= 0.39
BuildRequires:    mysql-devel, libxslt-devel, expat-devel, bzip2-devel, openldap-devel
BuildRequires:    elfutils-libelf-devel, binutils-devel, libevent-devel, ImageMagick-devel
BuildRequires:    libvpx-devel, libpng-devel, gmp-devel, ocaml, folly-devel
Provides:         hhvm-devel = %{version}-%{release}

%description devel
hhvm-devel contains the library links and header files you'll
need to develop HHVM applications.

%prep
%setup -q -n %{name}-%{version}

%build
export HPHP_HOME=`pwd`
export CPLUS_INCLUDE_PATH=/usr/include/libdwarf
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
%{__install} -p -D -m 0755 hphp/hack/bin/hh_client %{buildroot}%{_bindir}/hh_client
%{__install} -p -D -m 0755 hphp/hack/bin/hh_client %{buildroot}%{_bindir}/hh_server
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize %{buildroot}%{_bindir}/hphpize

# Install hhvm and systemctl configuration
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/hhvm/php.ini
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/hhvm/server.hdf
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/hhvm/config.hdf
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/hhvm.service

#devel
%{__mkdir} -p %{buildroot}%{_prefix}/lib64/hhvm
%{__mkdir} -p %{buildroot}%{_prefix}/lib64/hhvm/hphpize
%{__mkdir} -p %{buildroot}%{_prefix}/lib64/hhvm/CMake
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/runtime/base
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/runtime/ext
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/runtime/server
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/runtime/vm
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/neo
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/parser
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/system
%{__mkdir} -p %{buildroot}%{_prefix}/include/hphp/util
%{__mkdir} -p %{buildroot}%{_prefix}/man/man3
%{__mkdir} -p %{buildroot}%{_prefix}/share/doc/pcre/html

#header files
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize.cmake %{buildroot}%{_prefix}/lib64/hhvm/hphpize/hphpize.cmake
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize.cmake.in %{buildroot}%{_prefix}/lib64/hhvm/hphpize/hphpize.cmake.in
%{__install} -p -D -m 0755 CMake/*.cmake %{buildroot}%{_prefix}/lib64/hhvm/CMake
%{__install} -p -D -m 0755 third-party/pcre/libpcre.a %{buildroot}%{_prefix}/lib64/hhvm/libpcre.a
%{__install} -p -D -m 0755 third-party/pcre/libpcreposix.a %{buildroot}%{_prefix}/lib64/hhvm/libpcreposix.a
%{__install} -p -D -m 0755 third-party/pcre/libpcrecpp.a %{buildroot}%{_prefix}/lib64/hhvm/libpcrecpp.a
%{__install} -p -D -m 0755 third-party/pcre/pcre.h %{buildroot}%{_prefix}/include/hphp/pcre.h
%{__install} -p -D -m 0755 third-party/pcre/pcreposix.h %{buildroot}%{_prefix}/include/hphp/pcreposix.h
%{__install} -p -D -m 0755 third-party/pcre/pcrecpp.h %{buildroot}%{_prefix}/include/hphp/pcrecpp.h
%{__install} -p -D -m 0755 third-party/pcre/pcre_scanner.h %{buildroot}%{_prefix}/include/hphp/pcre_scanner.h
%{__install} -p -D -m 0755 third-party/pcre/pcrecpparg.h %{buildroot}%{_prefix}/include/hphp/pcrecpparg.h
%{__install} -p -D -m 0755 third-party/pcre/pcre_stringpiece.h %{buildroot}%{_prefix}/include/hphp/pcre_stringpiece.h
%{__install} -p -D -m 0755 hphp/neo/*.h %{buildroot}%{_prefix}/include/hphp/neo
%{__install} -p -D -m 0755 hphp/parser/*.h %{buildroot}%{_prefix}/include/hphp/parser
%{__install} -p -D -m 0755 hphp/runtime/base/*.h %{buildroot}%{_prefix}/include/hphp/runtime/base
%{__install} -p -D -m 0755 hphp/runtime/ext/*.h %{buildroot}%{_prefix}/include/hphp/runtime/ext
%{__install} -p -D -m 0755 hphp/runtime/server/*.h %{buildroot}%{_prefix}/include/hphp/runtime/server
%{__install} -p -D -m 0755 hphp/runtime/vm/*.h %{buildroot}%{_prefix}/include/hphp/runtime/vm
%{__install} -p -D -m 0755 hphp/system/*.h %{buildroot}%{_prefix}/include/hphp/system
%{__install} -p -D -m 0755 hphp/util/*.h %{buildroot}%{_prefix}/include/hphp/util

#man pages
%{__install} -p -D -m 0755 third-party/pcre/doc/*.3 %{buildroot}%{_prefix}/man/man3
%{__install} -p -D -m 0755 third-party/pcre/doc/html/*.html %{buildroot}%{_prefix}/share/doc/pcre/html

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{hhvm_group} >/dev/null || groupadd -r %{hhvm_group}
getent passwd %{hhvm_user} >/dev/null || \
    useradd -r -g %{hhvm_group} -d %{hhvm_dir} -s /sbin/nologin \
    -c "HHVM" %{hhvm_user}
exit 0

# Can't use -p /sbin/ldconfig, that gives '/sbin/ldconfig: relative path `0' used to build cache' error
%post
/sbin/ldconfig > /dev/null 2>&1
%systemd_post hhvm.service

%systemd_preun hhvm.service

# Can't use -p /sbin/ldconfig, that gives '/sbin/ldconfig: relative path `0' used to build cache' error
%postun
/sbin/ldconfig > /dev/null 2>&1
%systemd_postun hhvm.service

%files
%defattr(-,hhvm,hhvm,-)
%{_unitdir}/hhvm.service
%dir %{_var}/hhvm
%dir %{_var}/run/%{name}
%dir %{_var}/log/%{name}

%defattr(-,root,root,-)
%dir %{_sysconfdir}/hhvm
%config(noreplace) %{_sysconfdir}/hhvm/php.ini
%config(noreplace) %{_sysconfdir}/hhvm/server.hdf
%config(noreplace) %{_sysconfdir}/hhvm/config.hdf
%{_bindir}/hhvm
%{_bindir}/hh_client
%{_bindir}/hh_server
%{_bindir}/hphpize

%files devel
%defattr(-,root,root,-)
%{_prefix}/lib64/hhvm/hphpize/*
%{_prefix}/lib64/hhvm/CMake/*.cmake
%{_prefix}/lib64/hhvm/libpcre.a
%{_prefix}/lib64/hhvm/libpcreposix.a
%{_prefix}/lib64/hhvm/libpcrecpp.a
%{_prefix}/include/hphp/*

%{_prefix}/man/man3/*
%{_prefix}/share/doc/pcre/html/*

%doc CONTRIBUTING.md LICENSE.PHP LICENSE.ZEND README.md

%changelog
* Fri Sep 19 2014 Paul Moss <no1youknowz@gmail.com> - 3.3
- Initial built for el7
