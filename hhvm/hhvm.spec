#TODO: package pfff (https://github.com/facebook/pfff), so we can install hackificator and hack_remove_soft_types
#TODO: create debug package
#TODO: add aarch64 support
%define           hhvm_dir %{_var}/hhvm
%define           hhvm_group hhvm
%define           hhvm_user hhvm
%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm
Version:          3.4.2
Release:          3%{?dist}
Summary:          HipHop VM (HHVM) is a virtual machine for executing programs written in PHP
ExclusiveArch:    x86_64
Group:            Development/Languages
License:          PHP and Zend
URL:              http://hhvm.com
Source0:          https://github.com/facebook/hhvm/archive/%{name}-%{version}.tar.gz
Source1:          php.ini
Source2:          hhvm.service
# already applied upstream: https://github.com/facebook/hhvm/commit/3918a2ccceb98230ff517601ad60aa6bee36e2c4
Patch0:           replace-max-macro-with-std-max.patch
# already applied upstream: https://github.com/hhvm/hhvm-third-party/pull/39
Patch1:           3.4.x-use-system-libzip-and-pcre.patch
# not yet accepted upstream: https://github.com/hhvm/hhvm-third-party/pull/46
Patch2:           3.4.x-use-more-system-libs.patch
# not yet accepted upstream: https://github.com/facebook/hhvm/pull/4507
Patch3:           fix-debug-build-with-sqlite-3.8.x.patch
# not yet accepted upstream: https://github.com/facebook/hhvm/pull/4510
Patch4:           remove-sqlite-version-restriction.patch
BuildRequires:    cmake, libevent-devel
BuildRequires:    glog-devel, jemalloc-devel, tbb-devel
BuildRequires:    libmcrypt-devel, libdwarf-devel
BuildRequires:    libxml2-devel, libicu-devel, libcurl-devel
BuildRequires:    oniguruma-devel, readline-devel, double-conversion-devel
#BuildRequires:   libc-client-devel, pam-devel, gd-devel
BuildRequires:    libcap-devel, libedit-devel, pcre-devel, sqlite-devel
BuildRequires:    lz4-devel, fastlz-devel, fribidi-devel, libyaml-devel
BuildRequires:    boost-devel, libmemcached-devel
BuildRequires:    mysql-devel, libxslt-devel, expat-devel, bzip2-devel, openldap-devel
BuildRequires:    elfutils-libelf-devel, binutils-devel, libevent-devel, ImageMagick-devel
BuildRequires:    libvpx-devel, libpng-devel, gmp-devel, ocaml
BuildRequires:    json-c-devel
# libzip in EL 6-7 is too old, must use the bundled version
%if 0%{?fedora} >= 20
BuildRequires:    libzip-devel
%endif

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Requires:         systemd
Requires:         glog, jemalloc, tbb
Requires:         libmcrypt, libdwarf
Requires:         boost, libmemcached, lz4
Requires:         libxml2, libicu, oniguruma, readline, pam, libcap, libedit, pcre, sqlite
Requires:         libxslt, double-conversion, expat, bzip2, openldap, elfutils-libelf
Requires:         binutils, libevent, ImageMagick, libvpx, libpng, gmp, ocaml, libzip
Requires:         json-c, fastlz, fribidi, libyaml

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for executing
programs written in PHP.
HHVM uses a just-in-time compilation approach to achieve superior performance
while maintaining the flexibility that PHP developers are accustomed to.

%package          devel
Summary:          Library links and header files for HHVM development
Group:            Development/Libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
BuildRequires:    cmake, libevent-devel
BuildRequires:    libcurl-devel, double-conversion-devel
BuildRequires:    glog-devel, jemalloc-devel, tbb-devel
BuildRequires:    libmcrypt-devel, libdwarf-devel
BuildRequires:    libxml2-devel, libicu-devel, oniguruma-devel, readline-devel
BuildRequires:    libcap-devel, libedit-devel, pcre-devel, sqlite-devel
BuildRequires:    lz4-devel >= r121-2, fastlz-devel, fribidi-devel, libyaml-devel
BuildRequires:    boost-devel, libmemcached-devel
BuildRequires:    mysql-devel, libxslt-devel, expat-devel, bzip2-devel, openldap-devel
BuildRequires:    elfutils-libelf-devel, binutils-devel, libevent-devel, ImageMagick-devel
BuildRequires:    libvpx-devel, libpng-devel, gmp-devel, ocaml
Provides:         hhvm-devel = %{version}-%{release}

%description devel
hhvm-devel contains the library links and header files you'll
need to develop HHVM applications.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1
pushd third-party
%patch1 -p1
%patch2 -p1
popd
%patch3 -p1
%patch4 -p1

%build
export HPHP_HOME=`pwd`

cmake \
    -DUSE_JSONC=ON \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
    .

make %{?_smp_mflags}

%check
hphp/hhvm/hhvm hphp/test/run -m jit quick
hphp/hhvm/hhvm hphp/test/run -m interp quick

%install
export DONT_STRIP=1
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# Create default directory
# TODO: store pid and similar files in /run/hhvm/ instead of /var/run/hhvm
# https://fedoraproject.org/wiki/Packaging:Tmpfiles.d
%{__mkdir} -p %{buildroot}%{_var}/run/%{name}
%{__mkdir} -p %{buildroot}%{_var}/log/%{name}
%{__mkdir} -p %{buildroot}%{_var}/hhvm


# Install hhvm and systemctl configuration
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/hhvm/php.ini
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/hhvm.service

%{__mkdir} -p %{buildroot}%{_mandir}/man1

%{__install} -p -D -m 0644 hphp/doc/man/* %{buildroot}%{_mandir}/man1
%{__install} -p -D -m 0644 hphp/hack/man/* %{buildroot}%{_mandir}/man1

%{__mkdir} -p %{buildroot}%{_datadir}/hhvm

# TODO: maybe find some way to use /bin/install again?
%{__cp} -a  --preserve=timestamps hphp/hack/editor-plugins/ %{buildroot}%{_datadir}/hhvm/

# licenses
%{__mkdir} -p %{buildroot}%{_docdir}/hhvm/licenses

%{__install} -p -D -m 0644 third-party/folly/LICENSE %{buildroot}%{_docdir}/hhvm/licenses/folly
%{__install} -p -D -m 0644 third-party/fastlz/LICENSE %{buildroot}%{_docdir}/hhvm/licenses/fastlz
%{__install} -p -D -m 0644 third-party/libafdt/COPYING %{buildroot}%{_docdir}/hhvm/licenses/libafdt
%{__install} -p -D -m 0644 third-party/libmbfl/LICENSE %{buildroot}%{_docdir}/hhvm/licenses/libmbfl
# TODO: copy proxygen license when we 3.5.0 is released
%{__install} -p -D -m 0644 third-party/thrift/src/LICENSE %{buildroot}%{_docdir}/hhvm/licenses/thrift
# TODO: use the php license from timelib directly, when we bump to 3.5.0
%{__install} -p -D -m 0644 LICENSE.PHP %{buildroot}%{_docdir}/hhvm/licenses/timelib
%if 0%{?fedora} >= 20
%{__install} -p -D -m 0644 third-party/libzip/LICENSE %{buildroot}%{_docdir}/hhvm/licenses/libzip
%endif

%clean
rm -rf %{buildroot}

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

#%{_bindir}/hack_remove_soft_types
#%{_bindir}/hackificator
%{_bindir}/hh_client
%{_bindir}/hh_server
%{_bindir}/hhvm
%{_datadir}/hhvm/editor-plugins/*
%{_mandir}/man1/hackificator.1.gz
%{_mandir}/man1/hack_remove_soft_types.1.gz
%{_mandir}/man1/hh_client.1.gz
%{_mandir}/man1/hh_server.1.gz
%{_mandir}/man1/hhvm.1.gz
%doc CONTRIBUTING.md LICENSE.PHP LICENSE.ZEND README.md
%doc %{_docdir}/hhvm/licenses/*

%files devel
%defattr(-,root,root,-)
%{_prefix}/lib64/hhvm/hphpize/*
%{_prefix}/lib64/hhvm/CMake/*.cmake
%{_prefix}/include/hphp/*
%{_bindir}/hphpize
%{_mandir}/man1/hphpize.1.gz

%doc CONTRIBUTING.md LICENSE.PHP LICENSE.ZEND README.md
%doc %{_docdir}/hhvm/licenses/*

%changelog
* Fri Sep 19 2014 Paul Moss <no1youknowz@gmail.com> - 3.3
- Initial built for el7
