%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm-ext-zeromq
Version:          1.0
Release:          1%{?dist}
Summary:          ZeroMQ extension for HipHop VM

Group:            Development/Libraries
License:          PHP/Zend
URL:              https://github.com/no1youknowz/zmq-extension-for-hhvm
Source0:          %{name}.tar.gz
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, 
BuildRequires:    hhvm-devel, gflags-devel, libsodium-devel, zeromq-devel, tbb-devel
BuildRequires:    jemalloc-devel, glog-devel, double-conversion-devel, folly-devel, boost-devel

Requires:         zeromq

%description
ZeroMQ extension for HipHop VM

%prep
%setup -qc

%build
cd hhvm-ext-zeromq/zmq
/usr/local/bin/hphpize
cmake .
make

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p %{buildroot}/usr/local/lib64/hhvm/extensions
%{__install} -p -D -m 0755 hhvm-ext-zeromq/zmq/zmq.so %{buildroot}/usr/local/lib64/hhvm/extensions/zmq.so

%post
echo "To enable this extension:" > /dev/stderr
echo "Add to /etc/hhvm/php.ini" > /dev/stderr
echo "hhvm.dynamic_extensions[zmq] = zmq.so" > /dev/stderr

%files
%dir /usr/local/lib64/hhvm/extensions
/usr/local/lib64/hhvm/extensions/zmq.so

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT
