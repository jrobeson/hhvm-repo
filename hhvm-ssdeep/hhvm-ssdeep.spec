%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm-ext-ssdeep
Version:          1.1.0
Release:          1%{?dist}
Summary:          Ssdeep extension for HipHop VM

Group:            Development/Libraries
License:          PHP/Zend
URL:              https://github.com/reeze/msgpack-hhvm
Source0:          %{name}.tar.gz
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, tbb-devel, folly-devel, double-conversion-devel, ssdeep-devel
BuildRequires:    hhvm-devel, boost-devel, glog-devel, jemalloc-devel

%description
Ssdep extension for HipHop VM

%prep
%setup -qc

%build
cd hhvm-ext-ssdeep
/usr/local/bin/hphpize
cmake .
make

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p %{buildroot}/usr/local/lib64/hhvm/extensions
%{__install} -p -D -m 0755 hhvm-ext-ssdeep/ssdeep.so %{buildroot}/usr/local/lib64/hhvm/extensions/ssdeep.so

%files
%dir /usr/local/lib64/hhvm/extensions
/usr/local/lib64/hhvm/extensions/ssdeep.so

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT
