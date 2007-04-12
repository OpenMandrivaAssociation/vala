%define name vala
%define version 0.0.8
%define release %mkrel 1

%define major 0
%define libname %mklibname %name %major

Summary: Compiler for the GObject type system
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.paldo.org/vala/%{name}-%{version}.tar.bz2
License: LGPL
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

%package -n %libname-devel
Group: Development/Other
Summary: Vala development files
Requires: %libname = %version
Requires: %name = %version
Provides: libvala-devel = %version-%release
Provides: vala-devel = %version-%release

%description -n %libname-devel
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
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root)
%_libdir/libvala.so.%{major}*

%files -n %libname-devel
%defattr(-,root,root)
%doc ChangeLog
%_libdir/libvala.so
%_libdir/libvala.la
%_includedir/vala-1.0
%_libdir/pkgconfig/vala-1.0.pc

%files
%defattr(-,root,root)
%doc AUTHORS MAINTAINERS NEWS README
%_bindir/valac
%_datadir/%name


