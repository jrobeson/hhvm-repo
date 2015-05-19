%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm-ext-
Version:          1.1.0
Release:          1%{?dist}
Summary:          Aerospike extension for HipHop VM

Group:            Development/Libraries
License:          PHP/Zend
URL:              https://github.com/vipsoft/hhvm-ext-aerospike
Source0:          %{name}.tar.gz
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, tbb-devel, folly-devel, double-conversion-devel,
BuildRequires:    hhvm-devel, boost-devel, gflags-devel, glog-devel, jemalloc-devel, zlib-devel, aerospike-client-c

Requires:         aerospike

%description
Aerospike extension for HipHop VM

%prep
%setup -qc

%build
cd hhvm-ext-aerospike
/usr/bin/hphpize
cmake .
make

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p %{buildroot}/usr/lib64/hhvm/extensions
%{__install} -p -D -m 0755 hhvm-ext-aerospike/aerospike.so %{buildroot}/usr/lib64/hhvm/extensions/aerospike.so

%files
%dir /usr/lib64/hhvm/extensions
/usr/lib64/hhvm/extensions/aerospike.so

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT
