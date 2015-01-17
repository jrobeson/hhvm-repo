%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm-ext-zeromq
Version:          1.0
Release:          1%{?dist}
Summary:          GeoIP extension for HipHop VM

Group:            Development/Libraries
License:          PHP/Zend
URL:              https://github.com/duxet/hhvm-zmq
Source0:          %{name}.tar.gz
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7,
BuildRequires:    hhvm-devel, gflags-devel, libsodium-devel, zeromq-devel

Requires:         zeromq

%description
ZeroMQ extension for HipHop VM

%prep
%setup -qc

%build
cd hhvm-zmq
./build.sh

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p %{buildroot}%{_prefix}/lib64/hhvm/extensions
%{__install} -p -D -m 0755 hhvm-zmq/zmq.so %{buildroot}%{_prefix}/lib64/hhvm/extensions/zmq.so

%files
%dir %{_prefix}/lib64/hhvm/extensions
%{_prefix}/lib64/hhvm/extensions/zmq.so

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT
