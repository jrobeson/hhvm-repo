#TODO: package pfff (https://github.com/facebook/pfff), so we can install hackificator and hack_remove_soft_types
#TODO: create debug package
#TODO: add aarch64 support
#TODO: make sure hardened build is actually hardened
#TODO: snapshot builds
#TODO: filesystem or common package
#TODO: package up test runner? - https://github.com/hhvm/packaging/issues/93
#TODO: package vim-hack
#TODO: make  hhvm.service the best it can be
#TODO: switch to unix domain sockets by default
#TODO: make apache subpackage work on older versions
#TODO: see which Requires: are still valid
#TODO: install more documentation
#TODO: provide hhvm extension directory management as own package
#TODO: logrotate
%global           _hardened_build 1
%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

%{!?_httpd_confdir: %{expand: %%global _httpd_confdir %%{_sysconfdir}/httpd/conf.d}}
# httpd 2.4.10 with httpd-filesystem and sethandler support
%if 0%{?fedora} >= 21
%global with_httpd2410 1
%else
%global with_httpd2410 0
%endif

Name:             hhvm
Version:          3.5.0
Release:          2%{?dist}
Summary:          HipHop VM (HHVM) is a virtual machine for executing programs written in PHP
ExclusiveArch:    x86_64
Group:            Development/Languages
# TODO: check on more licenses
License:          PHP and Zend
URL:              http://hhvm.com
Source0:          https://github.com/facebook/hhvm/archive/%{name}-%{version}.tar.gz
Source1:          php.ini
Source2:          hhvm.service
Source3:          hhvm-tmpfiles.conf
Source4:          hhvm-apache.sysconfig
Source5:          hhvm-nginx.sysconfig
Source6:          nginx-hhvm.conf
Source7:          nginx-hhvm-location.conf
Source8:          apache-hhvm.conf
# already applied upstream: https://github.com/facebook/hhvm/commit/57e0e583f7fca06092eb64d9f70a0e2226708563
Patch1:           3.5.x-fix-mysql-cmake-finder-reporting.patch
# not submitted upstream until confirmation of false positive test:
# https://github.com/facebook/hhvm/issues/4136#issuecomment-68156016
Patch2:           remove-false-positive-array-dtor-test.patch
# not yet accepted upstream: https://github.com/facebook/hhvm/pull/4667
Patch3:           3.5.x-update-fsf-address-in-bcmath.patch
# not yet accepted upstream: https://github.com/hhvm/hhvm-third-party/pull/53
Patch4:           3.5.x-libmbfl-remove-spurious-exec-bit.patch

# chrpath is needed until this issue is solved: https://github.com/facebook/hhvm/issues/4654
# chrpath gets applied during make/make install
BuildRequires:    chrpath
BuildRequires:    cmake, libevent-devel
BuildRequires:    glog-devel, jemalloc-devel, tbb-devel
BuildRequires:    libmcrypt-devel, libdwarf-devel
BuildRequires:    libxml2-devel, libicu-devel, libcurl-devel
BuildRequires:    oniguruma-devel
BuildRequires:    libc-client-devel, pam-devel, gd-devel
BuildRequires:    libcap-devel, libedit-devel, pcre-devel, sqlite-devel
BuildRequires:    lz4-devel, fastlz-devel, fribidi-devel, libyaml-devel
BuildRequires:    boost-devel, libmemcached-devel
BuildRequires:    mysql-devel, libxslt-devel, expat-devel, bzip2-devel, openldap-devel
BuildRequires:    elfutils-libelf-devel, binutils-devel, libevent-devel, ImageMagick-devel
BuildRequires:    libvpx-devel, libpng-devel, gmp-devel, ocaml
BuildRequires:    json-c-devel, double-conversion-devel, libunwind-devel
%if 0%{?fedora}
# libzip in EL 6-7 is too old, must use the bundled version
BuildRequires:    libzip-devel >= 0.11
%endif

Requires:         pam, binutils, ocaml, fribidi

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for executing
programs written in PHP.
HHVM uses a just-in-time compilation approach to achieve superior performance
while maintaining the flexibility that PHP developers are accustomed to.

%package          apache
Summary:          Apache Configuration for HHVM
# TODO: pick the right group for apache subpackage
Group:            Development/Languages
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-fastcgi%{?_isa} = %{version}-%{release}
Conflicts:        %{name}-nginx%{?_isa}
%if %{with_httpd2410}
BuildRequires: httpd-filesystem
Requires:      httpd-filesystem
%else
BuildRequires: httpd
Requires:      httpd
%endif

%description apache
Apache configuration for HHVM

%package          devel
Summary:          Library links and header files for HHVM development
Group:            Development/Libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         cmake
Provides:         hhvm-devel = %{version}-%{release}

%description devel
hhvm-devel contains the library links and header files you'll
need to build and develop HHVM extensions.

%package          fastcgi
Summary:          FastCGI meta package for HHVM
# TODO: use the right group for fastcgi subpackage
Group:            Development/Libraries
BuildRequires:    systemd
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description fastcgi
FastCGI meta package for HHVM

%package          nginx
Summary:          Nginx Configuration for HHVM
# TODO: use the right group for nginx subpackage
Group:            Development/Languages
Requires:         %{name}-fastcgi%{?_isa} = %{version}-%{release}
Conflicts:        %{name}-apache%{?_isa}
BuildRequires:    nginx-filesystem
Requires:         nginx-filesystem

%description nginx
Nginx configuration for HHVM

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
pushd third-party
%patch4 -p1
popd

%build
cmake \
    -DUSE_JSONC=ON \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
    .

make %{?_smp_mflags}

%install
export DONT_STRIP=1
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/hhvm.conf

mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

mkdir -p %{buildroot}%{_sharedstatedir}/hhvm


# Install hhvm and systemctl configuration
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/hhvm/php.ini
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/hhvm.service
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/hhvm-apache
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/hhvm-nginx

# nginx
install -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/nginx/conf.d/hhvm.conf
install -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/nginx/default.d/hhvm.conf

# apache
%if %{with_httpd2410}
install -D -m 644 %{SOURCE8} %{buildroot}%{_httpd_confdir}/hhvm.conf
%endif

# man pages
mkdir -p %{buildroot}%{_mandir}/man1

install -p -D -m 0644 hphp/doc/man/* %{buildroot}%{_mandir}/man1
install -p -D -m 0644 hphp/hack/man/* %{buildroot}%{_mandir}/man1

# licenses
mkdir -p %{buildroot}%{_licensedir}/hhvm/licenses

install -p -D -m 0644 third-party/folly/LICENSE %{buildroot}%{_licensedir}/hhvm/folly
install -p -D -m 0644 third-party/libafdt/COPYING %{buildroot}%{_licensedir}/hhvm/libafdt
install -p -D -m 0644 third-party/libmbfl/LICENSE %{buildroot}%{_licensedir}/hhvm/libmbfl
install -p -D -m 0644 third-party/proxygen/src/LICENSE %{buildroot}%{_licensedir}/hhvm/proxygen
install -p -D -m 0644 third-party/thrift/src/LICENSE %{buildroot}%{_licensedir}/hhvm/thrift
install -p -D -m 0644 third-party/timelib/LICENSE %{buildroot}%{_licensedir}/hhvm/timelib
%if 0%{?rhel}
install -p -D -m 0644 third-party/libzip/LICENSE %{buildroot}%{_licensedir}/hhvm/libzip
%endif

%check
hphp/hhvm/hhvm hphp/test/run -m jit quick
hphp/hhvm/hhvm hphp/test/run -m interp quick

%clean
rm -rf %{buildroot}

%post fastcgi
%systemd_post hhvm.service

%preun fastcgi
%systemd_preun hhvm.service

%postun fastcgi
%systemd_postun hhvm.service

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/hhvm
%config(noreplace) %{_sysconfdir}/hhvm/php.ini

#%{_bindir}/hack_remove_soft_types
#%{_bindir}/hackificator
%{_bindir}/hh_client
%{_bindir}/hh_server
%{_bindir}/hhvm
%{_mandir}/man1/hackificator.1.*
%{_mandir}/man1/hack_remove_soft_types.1.*
%{_mandir}/man1/hh_client.1.*
%{_mandir}/man1/hh_server.1.*
%{_mandir}/man1/hhvm.1.*
%doc CONTRIBUTING.md README.md
%license LICENSE.PHP LICENSE.ZEND
%license %{_licensedir}/hhvm/*

%files apache
%attr(0770,root,apache) %dir %{_sharedstatedir}/hhvm
%attr(0770,apache,root) %dir %{_localstatedir}/log/hhvm
%config(noreplace) %{_sysconfdir}/sysconfig/hhvm-apache
%if %{with_httpd2410}
%config(noreplace) %{_httpd_confdir}/hhvm.conf
%endif
%files devel
%defattr(-,root,root,-)
%{_libdir}/hhvm/hphpize/*
%{_libdir}/hhvm/CMake/*.cmake
%{_includedir}/hphp/*
%{_bindir}/hphpize
%{_mandir}/man1/hphpize.1.*

%files fastcgi
%defattr(-,root,root,-)
%dir /run/hhvm/
%{_tmpfilesdir}/hhvm.conf
%{_unitdir}/hhvm.service

%files nginx
%attr(0770,root,nginx) %dir %{_sharedstatedir}/hhvm
%attr(0770,nginx,root) %dir %{_localstatedir}/log/hhvm
%config(noreplace) %{_sysconfdir}/nginx/conf.d/hhvm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/hhvm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/hhvm-nginx

%changelog
* Fri Sep 19 2014 Paul Moss <no1youknowz@gmail.com> - 3.3
- Initial built for el7
