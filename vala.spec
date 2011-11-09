%define api 0.14
%define major 0
%define libname %mklibname %name %api %major
%define libnamedev %mklibname -d %name

Summary: Compiler for the GObject type system
Name: vala
Version: 0.14.0
Release: 1
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/vala/%{name}-%{version}.tar.xz
# Most files are LGPLv2.1+, curses.vapi is 2-clause BSD
License: LGPLv2+ and BSD
Group: Development/Other
Url: http://live.gnome.org/Vala

BuildRequires: pkgconfig(glib-2.0) >= 2.25
BuildRequires: flex
BuildRequires: bison
#gw for make check: 
BuildRequires: dbus-glib-devel
# and why would this be needed for the main app?
#Requires: glib2-devel

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

%package -n %libname
Group: System/Libraries
Summary: Vala runtime library

%description -n %libname
This is the runtime library of the Vala programming language.

%package -n %libnamedev
Group: Development/Other
Summary: Vala development files
Requires: %libname = %version
Requires: %name = %version
Provides: libvala-devel = %version-%release
Provides: vala-devel = %version-%release
Obsoletes: %mklibname -d vala 0

%description -n %libnamedev
This is the development library of the Vala programming language.

%package tools
Summary: Tools for creating projects and bindings for %{name}
Group: Development/Other
Requires: %{name} = %{version}-%{release}
Requires: gnome-common intltool libtool

%description tools
This package contains tools to generate Vala projects, as well as API bindings
from existing C libraries, allowing access from Vala programs.

%prep
%setup -q
%apply_patches

%build
%configure2_5x --enable-vapigen
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %buildroot%_datadir/vala/vapi

%check
#gw checks don't run in iurt
#make check

%files -n %libname
%_libdir/libvala-%api.so.%{major}*

%files -n %libnamedev
%doc ChangeLog
%_libdir/libvala-%api.so
%_libdir/libvala-%api.la
%_includedir/vala-%api
%_libdir/pkgconfig/libvala-%api.pc
%_datadir/devhelp/books/vala-%api
%_datadir/aclocal/vala.m4

%files
%doc AUTHORS MAINTAINERS NEWS README
%_bindir/vala
%_bindir/vala-%api
%_bindir/valac
%_bindir/valac-%api
%_datadir/vala-%api
%dir %_datadir/vala
%dir %_datadir/vala/vapi
%_mandir/man1/valac.1*
%_mandir/man1/valac-%api.1*

%files tools
%{_bindir}/*gen*
%{_bindir}/vapicheck
%{_bindir}/vapicheck-%api
%{_libdir}/vala-%api
%{_mandir}/*/*gen*
