# TODO: adapt pfff to build with external libraries (see external for details)
# TODO: create a pfff-gtk package
%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%define debug_package %{nil}
%define _use_internal_dependency_generator 0
%define __find_requires /usr/lib/rpm/ocaml-find-requires.sh
%define __find_provides /usr/lib/rpm/ocaml-find-provides.sh

Name:           pfff
Version:        0.28.1
Release:        2%{?dist}
Summary:        Tools for code analysis, visualizations, or style-preserving source transformation.
Group:          Development/Libraries
License:        LGPLv2 with exceptions
URL:            https://github.com/facebook/%{name}
Source0:        https://github.com/facebook/%{name}/archive/v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       pl
BuildRequires:  ocaml, ocaml-findlib-devel
BuildRequires:  ocaml-camlp4, ocaml-camlp4-devel
BuildRequires:  perl-Pod-Usage
#BuildRequires:  gtk2-devel, atk-devel, pango-devel, cairo-devel
BuildRequires:  pl, ncurses-devel, binutils


%description
pfff is a set of tools and APIs to perform static analysis, code
visualizations, code navigations, or style-preserving source-to-source
transformations such as refactorings on source code.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        data
Summary:        Data files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    data
The %{name}-data package contains data files for developing
applications that use %{name}.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --novisual

make depend
make
%if %opt
make opt
%endif


%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}%{_libdir}/ocaml
export OCAMLFIND_LDCONF=%{buildroot}/tmp/ld.conf
mkdir -p $OCAMLFIND_DESTDIR
make install
make install-findlib


%clean
rm -rf %{buildroot}

%check
./pfff -dump_php demos/foo.php

%files
%defattr(-,root,root,-)
%doc readme.txt
%{_bindir}/*
%{_libdir}/ocaml/*
%if %opt
%exclude %{_libdir}/ocaml/*/*.a
%exclude %{_libdir}/ocaml/*/*.cmxa
%exclude %{_libdir}/ocaml/*/*.cmx
%endif
%exclude %{_libdir}/ocaml/*/*.mli

%files devel
%defattr(-,root,root,-)
%doc readme.txt
%exclude %{_bindir}/*
%exclude %{_datadir}/%{name}/*
%if %opt
%{_libdir}/ocaml/*/*.a
%{_libdir}/ocaml/*/*.cmxa
%{_libdir}/ocaml/*/*.cmx
%endif
%{_libdir}/ocaml/*/*.mli

%files data
%defattr(-,root,root,-)
%doc readme.txt
%{_datadir}/%{name}/

%changelog
* Sat Dec 27 2014 Johnny Robeson <johnny@localmomentum.net> - 0.28.1-1
- first try at a pfff spec
