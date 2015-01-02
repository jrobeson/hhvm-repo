#TODO: package pfff (https://github.com/facebook/pfff), so we can install hackificator and hack_remove_soft_types
#TODO: create debug package
#TODO: add aarch64 support
#TODO: hardened build
#TODO: snapshot builds
#TODO: filesystem or common package
%define           hhvm_dir %{_var}/hhvm
%define           hhvm_group hhvm
%define           hhvm_user hhvm
%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm
Version:          3.4.2
Release:          9%{?dist}
Summary:          HipHop VM (HHVM) is a virtual machine for executing programs written in PHP
ExclusiveArch:    x86_64
Group:            Development/Languages
License:          PHP and Zend
URL:              http://hhvm.com
Source0:          https://github.com/facebook/hhvm/archive/%{name}-%{version}.tar.gz
Source1:          php.ini
Source2:          hhvm.service
Source3:          %{name}-tmpfiles.conf
# already applied upstream: https://github.com/facebook/hhvm/commit/3918a2ccceb98230ff517601ad60aa6bee36e2c4
Patch0:           3.4.x-replace-max-macro-with-std-max.patch
# already applied upstream: https://github.com/hhvm/hhvm-third-party/pull/39
Patch1:           3.4.x-use-system-libzip-and-pcre.patch
# not yet accepted upstream: https://github.com/hhvm/hhvm-third-party/pull/46
Patch2:           3.4.x-use-more-system-libs.patch
# already applied upstream: https://github.com/facebook/hhvm/commit/b4ecc5de9675c692e76ec210a0618821190c3230
Patch3:           3.4.x-fix-debug-build-with-sqlite-3.8.x.patch
# already applied upstream: https://github.com/facebook/hhvm/commit/677fd774d259ece5a8bb1a5f58ac0d6ee1473a0f
Patch4:           3.4.x-remove-sqlite-version-restriction.patch
# already applied upstream: https://github.com/facebook/hhvm/commit/80cef006740e9f55b55728177d9ab6beb3a53ef9
Patch5:           3.4.x-add-fastlz-finder.patch
# not yet accepted upstream: https://github.com/facebook/hhvm/pull/4551
Patch6:           detect-fastlz-on-build.patch
# not submitted upstream until confirmation of false positive test:
# https://github.com/facebook/hhvm/issues/4136#issuecomment-68156016
Patch7:           remove-false-positive-array-dtor-test.patch
BuildRequires:    cmake, libevent-devel
BuildRequires:    glog-devel, jemalloc-devel, tbb-devel
BuildRequires:    libmcrypt-devel, libdwarf-devel
BuildRequires:    libxml2-devel, libicu-devel, libcurl-devel
BuildRequires:    oniguruma-devel, readline-devel
#BuildRequires:   libc-client-devel, pam-devel, gd-devel
BuildRequires:    libcap-devel, libedit-devel, pcre-devel, sqlite-devel
BuildRequires:    lz4-devel, fastlz-devel, fribidi-devel, libyaml-devel
BuildRequires:    boost-devel, libmemcached-devel
BuildRequires:    mysql-devel, libxslt-devel, expat-devel, bzip2-devel, openldap-devel
BuildRequires:    elfutils-libelf-devel, binutils-devel, libevent-devel, ImageMagick-devel
BuildRequires:    libvpx-devel, libpng-devel, gmp-devel, ocaml
BuildRequires:    json-c-devel, double-conversion-devel
%if 0%{?rhel}
# libzip in EL 6-7 is too old, must use the bundled version
BuildRequires:    libzip-devel
%endif

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Requires:         readline, pam, binutils, ocaml, fribidi

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for executing
programs written in PHP.
HHVM uses a just-in-time compilation approach to achieve superior performance
while maintaining the flexibility that PHP developers are accustomed to.

%package          devel
Summary:          Library links and header files for HHVM development
Group:            Development/Libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         cmake
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
%if 0%{?rhel}
# libzip in EL 6-7 is too old, must use the bundled version
BuildRequires:         libzip-devel
%endif
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
%patch5 -p1
%patch6 -p1
%patch7 -p1

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

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

%{__mkdir} -p %{buildroot}%{_var}/log/%{name}
%{__mkdir} -p %{buildroot}%{_var}/%{name}


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
%{__mkdir} -p %{buildroot}%{_licensedir}/hhvm/licenses

%{__install} -p -D -m 0644 third-party/folly/LICENSE %{buildroot}%{_licensedir}/hhvm/folly
%{__install} -p -D -m 0644 third-party/libafdt/COPYING %{buildroot}%{_licensedir}/hhvm/libafdt
%{__install} -p -D -m 0644 third-party/libmbfl/LICENSE %{buildroot}%{_licensedir}/hhvm/libmbfl
# TODO: copy proxygen license when we 3.5.0 is released
%{__install} -p -D -m 0644 third-party/thrift/src/LICENSE %{buildroot}%{_licensedir}/hhvm/thrift
# TODO: use the php license from timelib directly, when we bump to 3.5.0
%{__install} -p -D -m 0644 LICENSE.PHP %{buildroot}%{_licensedir}/hhvm/timelib
%if 0%{?rhel}
%{__install} -p -D -m 0644 third-party/libzip/LICENSE %{buildroot}%{_licensedir}/hhvm/libzip
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
%{_tmpfilesdir}/%{name}.conf
%dir /run/%{name}/
%dir %{_var}/%{name}
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
%doc CONTRIBUTING.md README.md
%license LICENSE.PHP LICENSE.ZEND
%license %{_licensedir}/hhvm/*

%files devel
%defattr(-,root,root,-)
%{_prefix}/lib64/hhvm/hphpize/*
%{_prefix}/lib64/hhvm/CMake/*.cmake
%{_prefix}/include/hphp/*
%{_bindir}/hphpize
%{_mandir}/man1/hphpize.1.gz

%doc CONTRIBUTING.md README.md
%license LICENSE.PHP LICENSE.ZEND

%changelog
* Fri Sep 19 2014 Paul Moss <no1youknowz@gmail.com> - 3.3
- Initial built for el7
