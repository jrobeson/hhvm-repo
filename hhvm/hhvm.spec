#TODO: package pfff (https://github.com/facebook/pfff), so we can install hackificator and hack_remove_soft_types
#TODO: snapshot builds
#TODO: filesystem or common package
#TODO: package up test runner? - https://github.com/hhvm/packaging/issues/93
#TODO: package vim-hack
#TODO: make  hhvm.service the best it can be
#TODO: switch to unix domain sockets by default
#TODO: make apache subpackage work on older versions
#TODO: install more documentation
#TODO: provide php alternative https://fedoraproject.org/wiki/Packaging:Alternatives
#TODO: find a way to get PEAR to work with hhvm, so we can provide php-common too.
%global _hardened_build 1
#TODO: remove undefine _includeminidebuginfo when patched rpm is available
#      https://bugzilla.redhat.com/show_bug.cgi?id=1186563
%undefine _include_minidebuginfo
%global _find_debuginfo_opts -g

%{!?_httpd_confdir: %{expand: %%global _httpd_confdir %%{_sysconfdir}/httpd/conf.d}}
# httpd 2.4.10 with httpd-filesystem and sethandler support
%if 0%{?fedora} >= 21
%global with_httpd2410 1
%else
%global with_httpd2410 0
%endif

#TODO: check to make sure hhvm/php API and php_version are bumped if changed upstream
%define php_api_version 20121113
%define hhvm_api_version 20150112
%define php_version 5.6.0
%define hhvm_extensiondir %{_libdir}/hhvm/extensions/%{hhvm_api_version}

Name:             hhvm
Version:          3.7.0
Release:          1%{?dist}
Summary:          HipHop VM (HHVM) is a virtual machine for executing programs written in PHP
ExclusiveArch:    x86_64
Group:            Development/Languages
License:          PHP and Zend and BSD and MIT and and ASL 2.0 and LGPLv2 with exceptions
URL:              http://hhvm.com
Source0:          https://github.com/facebook/hhvm/archive/%{name}-%{version}.tar.gz
Source1:          php.ini
Source2:          hhvm.service
Source3:          hhvm-tmpfiles.conf
Source4:          nginx-hhvm.conf
Source5:          nginx-hhvm-location.conf
Source6:          apache-hhvm.conf
Source7:          hhvm.logrotate
Source8:          macros.hhvm
# upstream is still in discussion in regards to accepting this:
# https://github.com/hhvm/hhvm-third-party/pull/40
Patch1:           use-system-tzinfo.patch
# not submitted upstream until confirmation of false positive test:
# https://github.com/facebook/hhvm/issues/4136#issuecomment-68156016
Patch2:           remove-false-positive-array-dtor-test.patch

# needed to fix rpmlint W: executable-stack https://github.com/facebook/hhvm/issues/4704
BuildRequires:    prelink
BuildRequires:    flex, bison
BuildRequires:    cmake, libevent-devel, openssl-devel
BuildRequires:    glog-devel, jemalloc-devel, tbb-devel
BuildRequires:    libmcrypt-devel, libdwarf-devel
BuildRequires:    libxml2-devel, libicu-devel, libcurl-devel
BuildRequires:    oniguruma-devel, unixODBC-devel
BuildRequires:    libc-client-devel, pam-devel, gd-devel
BuildRequires:    libcap-devel, libedit-devel, pcre-devel, sqlite-devel
BuildRequires:    lz4-devel, fastlz-devel, fribidi-devel, libyaml-devel
BuildRequires:    boost-devel, libmemcached-devel, readline-devel
BuildRequires:    mysql-devel, libxslt-devel, expat-devel, bzip2-devel, openldap-devel
BuildRequires:    elfutils-libelf-devel, binutils-devel, libevent-devel, ImageMagick-devel
BuildRequires:    libvpx-devel, libpng-devel, gmp-devel, ocaml, ocaml-findlib
BuildRequires:    json-c-devel, double-conversion-devel, libunwind-devel
%if 0%{?fedora}
# libzip in EL 6-7 is too old, must use the bundled version
BuildRequires:    libzip-devel >= 0.11
%endif

# HHVM specific provides
Provides:         hhvm(api) = %{hhvm_api_version}
Provides:         hhvm(array_tracer), hhvm(array_tracer)%{?_isa}
Provides:         hhvm(asio), hhvm(asio)%{?_isa}
Provides:         hhvm(enum), hhvm(enum)%{?_isa}
Provides:         hhvm(fb), hhvm(fb)%{?_isa}
Provides:         hvvm(hh), hhvm(hh)%{?_isa}
Provides:         hhvm(hhvm.debugger), hhvm(hhvm.debugger)%{?_isa}
Provides:         hhvm(hhvm.ini), hhvm(hhvm.ini)%{?_isa}
Provides:         hhvm(hotprofiler), hhvm(hotprofiler)%{?_isa}
Provides:         hhvm(objprof), hhvm(objprof)%{?_isa}
Provides:         hhvm(server), hhvm(server)%{?_isa}
Provides:         hhvm(xenon), hhvm(xenon)%{?_isa}

# PHP global provides
Provides:         php(language) = %{php_version}, php(language)%{?_isa} = %{php_version}
Provides:         php(api) = %{php_api_version}%{isasuffix}
Provides:         php_database
Provides:         php-process
# PHP module provides
# hhvm --php -r 'foreach (get_loaded_extensions() as $ext) echo sprintf('"'"'Provides:         php-%1$s, php-%1$s%%{?_isa}, hhvm(%1$s), hhvm(%1$s)%%{?_isa}'"'".PHP_EOL', strtolower($ext));'
# This list will contain hhvm only modules. TODO: filter them out.
# Provides for builtin modules (php uses php-foo over php(foo) for historical reasons)
Provides:         php-apc, php-apc%{?_isa}, hhvm(apc), hhvm(apc)%{?_isa}
Provides:         php-array, php-array%{?_isa}, hhvm(array), hhvm(array)%{?_isa}
Provides:         php-bcmath, php-bcmath%{?_isa}, hhvm(bcmath), hhvm(bcmath)%{?_isa}
Provides:         php-bz2, php-bz2%{?_isa}, hhvm(bz2), hhvm(bz2)%{?_isa}
Provides:         php-ctype, php-ctype%{?_isa}, hhvm(ctype), hhvm(ctype)%{?_isa}
Provides:         php-curl, php-curl%{?_isa}, hhvm(curl), hhvm(curl)%{?_isa}
Provides:         php-date, php-date%{?_isa}, hhvm(date), hhvm(date)%{?_isa}
Provides:         php-debugger, php-debugger%{?_isa}, hhvm(debugger), hhvm(debugger)%{?_isa}
Provides:         php-dom, php-dom%{?_isa}, hhvm(dom), hhvm(dom)%{?_isa}
Provides:         php-domdocument, php-domdocument%{?_isa}, hhvm(domdocument), hhvm(domdocument)%{?_isa}
Provides:         php-exif, php-exif%{?_isa}, hhvm(exif), hhvm(exif)%{?_isa}
Provides:         php-fileinfo, php-fileinfo%{?_isa}, hhvm(fileinfo), hhvm(fileinfo)%{?_isa}
Provides:         php-filter, php-filter%{?_isa}, hhvm(filter), hhvm(filter)%{?_isa}
Provides:         php-gd, php-gd%{?_isa}, hhvm(gd), hhvm(gd)%{?_isa}
Provides:         php-gmp, php-gmp%{?_isa}, hhvm(gmp), hhvm(gmp)%{?_isa}
Provides:         php-hash, php-hash%{?_isa}, hhvm(hash), hhvm(hash)%{?_isa}
Provides:         php-iconv, php-iconv%{?_isa}, hhvm(iconv), hhvm(iconv)%{?_isa}
Provides:         php-idn, php-idn%{?_isa}, hhvm(idn), hhvm(idn)%{?_isa}
Provides:         php-imagick, php-imagick%{?_isa}, hhvm(imagick), hhvm(imagick)%{?_isa}
Provides:         php-imap, php-imap%{?_isa}, hhvm(imap), hhvm(imap)%{?_isa}
Provides:         php-intl, php-intl%{?_isa}, hhvm(intl), hhvm(intl)%{?_isa}
Provides:         php-json, php-json%{?_isa}, hhvm(json), hhvm(json)%{?_isa}
Provides:         php-ldap, php-ldap%{?_isa}, hhvm(ldap), hhvm(ldap)%{?_isa}
Provides:         php-libxml, php-libxml%{?_isa}, hhvm(libxml), hhvm(libxml)%{?_isa}
Provides:         php-mail, php-mail%{?_isa}, hhvm(mail), hhvm(mail)%{?_isa}
Provides:         php-mailparse, php-mailparse%{?_isa}, hhvm(mailparse), hhvm(mailparse)%{?_isa}
Provides:         php-mbstring, php-mbstring%{?_isa}, hhvm(mbstring), hhvm(mbstring)%{?_isa}
Provides:         php-mcrypt, php-mcrypt%{?_isa}, hhvm(mcrypt), hhvm(mcrypt)%{?_isa}
Provides:         php-memcache, php-memcache%{?_isa}, hhvm(memcache), hhvm(memcache)%{?_isa}
Provides:         php-memcached, php-memcached%{?_isa}, hhvm(memcached), hhvm(memcached)%{?_isa}
Provides:         php-mysql, php-mysql%{?_isa}, hhvm(mysql), hhvm(mysql)%{?_isa}
Provides:         php-mysqli, php-mysqli%{?_isa}, hhvm(mysqli), hhvm(mysqli)%{?_isa}
Provides:         php-openssl, php-openssl%{?_isa}, hhvm(openssl), hhvm(openssl)%{?_isa}
Provides:         php-pcntl, php-pcntl%{?_isa}, hhvm(pcntl), hhvm(pcntl)%{?_isa}
Provides:         php-pcre, php-pcre%{?_isa}, hhvm(pcre), hhvm(pcre)%{?_isa}
Provides:         php-pdo, php-pdo%{?_isa}, hhvm(pdo), hhvm(pdo)%{?_isa}
Provides:         php-pdo_mysql, php-pdo_mysql%{?_isa}, hhvm(pdo_mysql), hhvm(pdo_mysql)%{?_isa}
Provides:         php-pdo_sqlite, php-pdo_sqlite%{?_isa}, hhvm(pdo_sqlite), hhvm(pdo_sqlite)%{?_isa}
Provides:         php-phar, php-phar%{?_isa}, hhvm(phar), hhvm(phar)%{?_isa}
Provides:         php-posix, php-posix%{?_isa}, hhvm(posix), hhvm(posix)%{?_isa}
Provides:         php-readline, php-readline%{?_isa}, hhvm(readline), hhvm(readline)%{?_isa}
Provides:         php-redis, php-redis%{?_isa}, hhvm(redis), hhvm(redis)%{?_isa}
Provides:         php-reflection, php-reflection%{?_isa}, hhvm(reflection), hhvm(reflection)%{?_isa}
Provides:         php-server, php-server%{?_isa}, hhvm(server), hhvm(server)%{?_isa}
Provides:         php-session, php-session%{?_isa}, hhvm(session), hhvm(session)%{?_isa}
Provides:         php-simplexml, php-simplexml%{?_isa}, hhvm(simplexml), hhvm(simplexml)%{?_isa}
Provides:         php-soap, php-soap%{?_isa}, hhvm(soap), hhvm(soap)%{?_isa}
Provides:         php-sockets, php-sockets%{?_isa}, hhvm(sockets), hhvm(sockets)%{?_isa}
Provides:         php-spl, php-spl%{?_isa}, hhvm(spl), hhvm(spl)%{?_isa}
Provides:         php-sqlite3, php-sqlite3%{?_isa}, hhvm(sqlite3), hhvm(sqlite3)%{?_isa}
Provides:         php-standard, php-standard%{?_isa}, hhvm(standard), hhvm(standard)%{?_isa}
Provides:         php-stream, php-stream%{?_isa}, hhvm(stream), hhvm(stream)%{?_isa}
Provides:         php-string, php-string%{?_isa}, hhvm(string), hhvm(string)%{?_isa}
Provides:         php-sysvmsg, php-sysvmsg%{?_isa}, hhvm(sysvmsg), hhvm(sysvmsg)%{?_isa}
Provides:         php-sysvsem, php-sysvsem%{?_isa}, hhvm(sysvsem), hhvm(sysvsem)%{?_isa}
Provides:         php-sysvshm, php-sysvshm%{?_isa}, hhvm(sysvshm), hhvm(sysvshm)%{?_isa}
Provides:         php-thread, php-thread%{?_isa}, hhvm(thread), hhvm(thread)%{?_isa}
Provides:         php-thrift_protocol, php-thrift_protocol%{?_isa}, hhvm(thrift_protocol), hhvm(thrift_protocol)%{?_isa}
Provides:         php-tokenizer, php-tokenizer%{?_isa}, hhvm(tokenizer), hhvm(tokenizer)%{?_isa}
Provides:         php-url, php-url%{?_isa}, hhvm(url), hhvm(url)%{?_isa}
Provides:         php-wddx, php-wddx%{?_isa}, hhvm(wddx), hhvm(wddx)%{?_isa}
Provides:         php-xhprof, php-xhprof%{?_isa}, hhvm(xhprof), hhvm(xhprof)%{?_isa}
Provides:         php-xml, php-xml%{?_isa}, hhvm(xml), hhvm(xml)%{?_isa}
Provides:         php-xmlreader, php-xmlreader%{?_isa}, hhvm(xmlreader), hhvm(xmlreader)%{?_isa}
Provides:         php-xmlwriter, php-xmlwriter%{?_isa}, hhvm(xmlwriter), hhvm(xmlwriter)%{?_isa}
Provides:         php-xsl, php-xsl%{?_isa}, hhvm(xsl), hhvm(xsl)%{?_isa}
Provides:         php-zip, php-zip%{?_isa}, hhvm(zip), hhvm(zip)%{?_isa}
Provides:         php-zlib, php-zlib%{?_isa}, hhvm(zlib), hhvm(zlib)%{?_isa}

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for executing
programs written in PHP.
HHVM uses a just-in-time compilation approach to achieve superior performance
while maintaining the flexibility that PHP developers are accustomed to.

%package          apache
Summary:          Apache Configuration for HHVM
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
Requires:         cmake, gdb
Provides:         hhvm-devel = %{version}-%{release}

%description devel
hhvm-devel contains the library links and header files you'll
need to build and develop HHVM extensions.

%package          fastcgi
Summary:          FastCGI meta package for HHVM
Group:            Development/Languages
BuildRequires:    systemd
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         systemd
Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description fastcgi
FastCGI meta package for HHVM

%package          nginx
Summary:          Nginx Configuration for HHVM
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

%pre fastcgi
getent group hhvm >/dev/null || groupadd -r hhvm
getent passwd hhvm >/dev/null || \
    useradd -r -g hhvm -d /var/lib/hhvm -s /sbin/nologin \
    -c "HHVM" hhvm
exit 0

%build
# Fixes https://github.com/facebook/hhvm/issues/4705
LDFLAGS="$LDFLAGS -Wl,--as-needed"
export LDFLAGS

%cmake \
    -DUSE_JSONC:BOOL=ON \
    -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
    -DMYSQL_UNIX_SOCK_ADDR=/var/lib/mysql/mysql.sock \
    .

./hphp/parser/make-lexer.sh
./hphp/parser/make-parser.sh

make %{?_smp_mflags}

mkdir strip-wrapper
#TODO: remove overridden eu-strip when patched rpm is available
#      https://bugzilla.redhat.com/show_bug.cgi?id=1186563
cat > strip-wrapper/eu-strip <<'EOF'
#!/bin/bash
STRIP_ARGS=""
case "$*" in
    */hhvm|*/hh_client|*/hh_server)
        STRIP_ARGS="-g"
        ;;
esac
exec /usr/bin/eu-strip "$STRIP_ARGS" "$@"
EOF
chmod +x strip-wrapper/eu-strip

%install
PATH="$(pwd)/strip-wrapper:$PATH"

rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

execstack -c %{buildroot}%{_bindir}/hhvm

%{__mkdir_p} %{buildroot}%{hhvm_extensiondir}

%{__mkdir_p} %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/hhvm.conf

%{__mkdir_p} %{buildroot}/run
install -d -m 0755 %{buildroot}/run/hhvm/

%{__mkdir_p} %{buildroot}%{_localstatedir}/log/hhvm

%{__mkdir_p} %{buildroot}%{_sharedstatedir}/hhvm

# Install hhvm and systemctl configuration
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/hhvm/php.ini
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/hhvm.service

# nginx
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/nginx/conf.d/hhvm.conf
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/nginx/default.d/hhvm.conf

# apache
%if %{with_httpd2410}
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_httpd_confdir}/hhvm.conf
%endif

# Logrotate configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/hhvm

# RPM Macros
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rpm
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/rpm/macros.hhvm
# perform substitutions appropriately
%{__sed} -i "s#HHVM_API_VERSION#%{hhvm_api_version}#" %{buildroot}%{_sysconfdir}/rpm/macros.hhvm
%{__sed} -i "s#HHVM_PHP_VERSION#%{php_version}#" %{buildroot}%{_sysconfdir}/rpm/macros.hhvm
%{__sed} -i "s#HHVM_PHP_API_VERSION#%{php_api_version}#" %{buildroot}%{_sysconfdir}/rpm/macros.hhvm
%{__sed} -i "s#HHVM_EXTENSION_DIR#%{hhvm_extensiondir}#" %{buildroot}%{_sysconfdir}/rpm/macros.hhvm
%{__sed} -i "s#HPHPIZE#%{_bindir}/hphpize#" %{buildroot}%{_sysconfdir}/rpm/macros.hhvm

# man pages
%{__mkdir_p} %{buildroot}%{_mandir}/man1

install -p -D -m 0644 hphp/doc/man/* %{buildroot}%{_mandir}/man1
install -p -D -m 0644 hphp/hack/man/* %{buildroot}%{_mandir}/man1

# licenses
%{__mkdir_p} %{buildroot}%{_licensedir}/hhvm/licenses

# bundled code licenses
install -p -D -m 0644 hphp/runtime/ext/fileinfo/libmagic/LICENSE %{buildroot}%{_licensedir}/hhvm/libmagic_LICENSE
install -p -D -m 0644 hphp/runtime/ext/gd/libgd/COPYING %{buildroot}%{_licensedir}/hhvm/libgd_COPYING
install -p -D -m 0644 hphp/runtime/ext_zend_compat/oauth/LICENSE %{buildroot}%{_licensedir}/hhvm/oauth_LICENSE
install -p -D -m 0644 hphp/neo/license.hdf %{buildroot}%{_licensedir}/hhvm/neo_LICENSE
install -p -D -m 0644 hphp/test/frameworks/spyc/COPYING %{buildroot}%{_licensedir}/hhvm/spyc_COPYING
install -p -D -m 0644 hphp/test/server/fastcgi/Adoy/LICENSE %{buildroot}%{_licensedir}/hhvm/adoy_LICENSE
install -p -D -m 0644 hphp/test/slow/ext_imagick/php_imagick_tests/LICENSE %{buildroot}%{_licensedir}/hhvm/ext_imagick_LICENSE
install -p -D -m 0644 hphp/hack/LICENSE %{buildroot}%{_licensedir}/hhvm/hack_LICENSE
install -p -D -m 0644 hphp/hack/src/third-party/avl/LICENSE %{buildroot}%{_licensedir}/hhvm/avl_LICENSE
install -p -D -m 0644 hphp/hack/src/third-party/inotify/LICENSE %{buildroot}%{_licensedir}/hhvm/inotify_LICENSE
# third party separable licenses
install -p -D -m 0644 third-party/folly/LICENSE %{buildroot}%{_licensedir}/hhvm/folly_LICENSE
install -p -D -m 0644 third-party/libafdt/COPYING %{buildroot}%{_licensedir}/hhvm/libafdt_COPYING
install -p -D -m 0644 third-party/libmbfl/LICENSE %{buildroot}%{_licensedir}/hhvm/libmbfl_LICENSE
install -p -D -m 0644 third-party/proxygen/src/LICENSE %{buildroot}%{_licensedir}/hhvm/proxygen_LICENSE
install -p -D -m 0644 third-party/thrift/src/LICENSE %{buildroot}%{_licensedir}/hhvm/thrift_LICENSE
install -p -D -m 0644 third-party/timelib/LICENSE %{buildroot}%{_licensedir}/hhvm/timelib_LICENSE
%if 0%{?rhel}
install -p -D -m 0644 third-party/libzip/LICENSE %{buildroot}%{_licensedir}/hhvm/libzip_LICENSE
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
%dir %{hhvm_extensiondir}
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
%if %{with_httpd2410}
%config(noreplace) %{_httpd_confdir}/hhvm.conf
%endif

%files devel
%defattr(-,root,root,-)
#TODO: temp exclude until we know the name of the test runner
%exclude %{_libdir}/hhvm/hphpize/run
%{_libdir}/hhvm/hphpize/*.cmake
%{_libdir}/hhvm/gdb/*
%{_libdir}/hhvm/CMake/*.cmake
%{_includedir}/hphp/*
%{_bindir}/hhvm-gdb
%{_bindir}/hphpize
%{_mandir}/man1/hphpize.1.*
# RPM macros
%{_sysconfdir}/rpm/macros.hhvm

%files fastcgi
%defattr(-,root,root,-)
%ghost %dir /run/hhvm/
%attr(0770,hhvm,hhvm) %dir %{_localstatedir}/log/hhvm
%attr(0770,hhvm,hhvm) %dir %{_sharedstatedir}/hhvm
%config(noreplace) %{_sysconfdir}/logrotate.d/hhvm
%{_tmpfilesdir}/hhvm.conf
%{_unitdir}/hhvm.service

%files nginx
%config(noreplace) %{_sysconfdir}/nginx/conf.d/hhvm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/hhvm.conf

%changelog
* Fri Sep 19 2014 Paul Moss <no1youknowz@gmail.com> - 3.3
- Initial built for el7
