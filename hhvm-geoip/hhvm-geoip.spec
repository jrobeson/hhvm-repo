%global           _enable_debug_package 0
%global           debug_package %{nil}
%global           __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             hhvm-ext-geoip
Version:          1.1.0
Release:          1%{?dist}
Summary:          GeoIP extension for HipHop VM

Group:            Development/Libraries
License:          PHP/Zend
URL:              https://github.com/vipsoft/hhvm-ext-geoip
Source0:          %{name}.tar.gz
BuildRequires:    gcc >= 4.7.2, cmake >= 2.8.7, tbb-devel, folly-devel, double-conversion-devel,
BuildRequires:    hhvm-devel, boost-devel, glog-devel, jemalloc-devel, zlib-devel, GeoIP-devel

Requires:         GeoIP

%description
GeoIP extension for HipHop VM

%prep
%setup -qc
%patch0 -p0

%build
cd hhvm-ext-geoip
/usr/local/bin/hphpize
cmake .
make

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p %{buildroot}/usr/local/lib64/hhvm/extensions
%{__install} -p -D -m 0755 hhvm-ext-geoip/geoip.so %{buildroot}/usr/local/lib64/hhvm/extensions/geoip.so

%files
%dir /usr/local/lib64/hhvm/extensions
/usr/local/lib64/hhvm/extensions/geoip.so

# Cleanup

%clean
rm -rf $RPM_BUILD_ROOT
