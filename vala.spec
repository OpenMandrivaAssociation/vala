%define name vala
%define version 0.5.4
%define release %mkrel 1

%define major 0
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name

Summary: Compiler for the GObject type system
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/vala/%{name}-%{version}.tar.bz2
# Most files are LGPLv2.1+, curses.vapi is 2-clause BSD
License: LGPLv2+ and BSD
Group: Development/Other
Url: http://live.gnome.org/Vala
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: glib2-devel
BuildRequires: flex
BuildRequires: bison

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

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%check
# http://bugzilla.gnome.org/show_bug.cgi?id=562951
#make check

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root)
%_libdir/libvala.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%doc ChangeLog
%_libdir/libvala.so
%_libdir/libvala.la
%_includedir/vala-1.0
%_libdir/pkgconfig/vala-1.0.pc
%_datadir/devhelp/books/vala

%files
%defattr(-,root,root)
%doc AUTHORS MAINTAINERS NEWS README
%_bindir/valac
%_datadir/%name
%_mandir/man1/valac.1*
