%define url_ver %(echo %{version}|cut -d. -f1,2)


%define api	0.56
%define major	0
%define libname	%mklibname %{name} %{api} %major
%define	devname	%mklibname -d %{name}
%define libdoc	%mklibname valadoc %{api} %{major}
%define devdoc	%mklibname valadoc -d

%bcond_with	check


Summary:	Compiler for the GObject type system
Name:		vala
Version:	0.56.1
Release:	1
# Most files are LGPLv2.1+, curses.vapi is 2-clause BSD
License:	LGPLv2+ and BSD
Group:		Development/Other
Url:		http://live.gnome.org/Vala
Source0:	http://ftp.gnome.org/pub/GNOME/sources/vala/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(glib-2.0) >= 2.25
BuildRequires:	pkgconfig(libgvc)
%if %{with check}
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	dbus-x11
%endif

%description
Vala is a new programming language that aims to bring modern
programming language features to GNOME developers without imposing any
additional runtime requirements and without using a different ABI
compared to applications and libraries written in C.

valac, the Vala compiler, is a self-hosting compiler that translates
Vala source code into C source and header files. It uses the GObject
type system to create classes and interfaces declared in the Vala
source code. It's also planned to generate GIDL files when
gobject-introspection is ready.

The syntax of Vala is similar to C#, modified to better fit the GObject
type system. Vala supports modern language features as the following:

* Interfaces
* Properties
* Signals
* Foreach
* Lambda expressions
* Type inference for local variables
* Non-null types [PARTIAL]
* Exception handling [PLANNED]
* Assisted memory management

* type modules (aka. Plugins)

Vala is designed to allow access to existing C libraries, especially
GObject-based libraries, without the need for runtime bindings. Each
to be used library requires a Vala API file at compile-time,
containing the class and method declarations in Vala syntax. Vala
currently comes with experimental bindings for GLib and GTK+. It's
planned to provide generated bindings for the full GNOME Platform at a
later stage.

Using classes and methods written in Vala from an application written
in C is not difficult. The Vala library only has to install the
generated header files and C applications may then access the
GObject-based API of the Vala library as usual. It should also be
easily possible to write a bindings generator for access to Vala
libraries from applications written in e.g. C# as the Vala parser is written
as a library, so that all compile-time information is available when
generating a binding.

%package -n %{libname}
Group:		System/Libraries
Summary:	Vala runtime library

%description -n %{libname}
This is the runtime library of the Vala programming language.


%package -n     valadoc
Summary:        Vala documentation generator
Group:		Documentation
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n valadoc
Valadoc is a documentation generator for generating API documentation from Vala
source code.

%package -n	%{libdoc}
Summary:	Shared libraries for valadoc
Group:		System/Libraries
Conflicts:	valadoc < 0.38.1-4

%description -n	%{libdoc}
Valadoc is a documentation generator for generating API documentation from Vala
source code.

%package -n     %{devdoc}
Summary:        Development files for valadoc
Group:		Development/Other
Requires:       %{libdoc} = %{version}-%{release}
Requires:	valadoc = %{version}-%{release}
Obsoletes:	valadoc-devel < 0.38.1-4
Provides:	valadoc-devel = %{version}-%{release}

%description -n %{devdoc}
Valadoc is a documentation generator for generating API documentation from Vala
source code.

This package contains development libraries and header files for
developing applications that use valadoc.

%package -n %{devname}
Group:		Development/Other
Summary:	Vala development files
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-tools = %{version}-%{release}
Provides:	vala-devel = %{version}-%{release}
Obsoletes:	%mklibname -d vala 0

%description -n %{devname}
This is the development library of the Vala programming language.

%package tools
Summary:	Tools for creating projects and bindings for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Requires:	intltool
Requires:	libtool

%description tools
This package contains tools to generate Vala projects, as well as API bindings
from existing C libraries, allowing access from Vala programs.

%prep
%setup -q
%autopatch -p1

%build
%configure \
	--enable-vapigen

%make_build

%install
%make_install

mkdir -p %{buildroot}%{_datadir}/vala/vapi

%if %{with check}
%check
%make check
%endif

%files
%doc NEWS README
%{_bindir}/vala
%{_bindir}/vala-%{api}
%{_bindir}/valac
%{_bindir}/valac-%{api}
%{_datadir}/vala-%{api}
%dir %{_datadir}/vala
%{_datadir}/vala/vapi/*
%{_mandir}/man1/valac.1*
%{_mandir}/man1/valac-%{api}.1*
%{_mandir}/man1/valadoc*

%files -n %{libname}
%{_libdir}/libvala-%{api}.so.%{major}*

%files -n %{devname}
%doc ChangeLog AUTHORS
%{_includedir}/vala-%{api}
%{_libdir}/libvala-%{api}.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/devhelp/books/vala-%{api}
%{_datadir}/aclocal/*.m4

%files -n valadoc
%{_bindir}/valadoc
%{_bindir}/valadoc-%{api}
%{_libdir}/valadoc-%{api}/
%{_datadir}/valadoc-%{api}/
%{_mandir}/man1/valadoc-%{api}.1*
%{_mandir}/man1/valadoc.1*

%files -n %{libdoc}
%{_libdir}/libvaladoc-%{api}.so.%{major}
%{_libdir}/libvaladoc-%{api}.so.%{major}.*

%files -n %{devdoc}
%{_includedir}/valadoc-%{api}/
%{_libdir}/libvaladoc-%{api}.so
%{_libdir}/pkgconfig/valadoc-%{api}.pc

%files tools
%{_bindir}/*gen*
#{_bindir}/vapicheck
#{_bindir}/vapicheck-%{api}
%{_datadir}/vala/Makefile.vapigen
%{_libdir}/vala-%{api}
%{_mandir}/*/*gen*

