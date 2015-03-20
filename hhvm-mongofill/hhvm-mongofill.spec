%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm-ext-mongofill
Version:          1.1.0
Release:          1%{?dist}
Summary:          Mongofill extension for HipHop VM

Group:            Development/Libraries
License:          PHP/Zend
URL:              https://github.com/mongofill/mongofill-hhvm
Source0:          %{name}.tar.gz
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, tbb-devel, folly-devel, double-conversion-devel, zlib-devel
BuildRequires:    hhvm-devel, boost-devel, glog-devel, jemalloc-devel, gflags-devel

%description
Mongofill extension for HipHop VM

%prep
%setup -qc

%build
# run this and then pack tarball 
# set -ev
# git submodule update --init
# hhvm tools/merge.php

cd hhvm-ext-mongofill
/usr/local/bin/hphpize
cmake .
make

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p %{buildroot}/usr/local/lib64/hhvm/extensions
%{__install} -p -D -m 0755 hhvm-ext-mongofill/mongo.so %{buildroot}/usr/local/lib64/hhvm/extensions/mongo.so

%files
%dir /usr/local/lib64/hhvm/extensions
/usr/local/lib64/hhvm/extensions/mongo.so

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT
