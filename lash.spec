%define name	lash
%define version	0.5.4
%define release %mkrel 1

%define major	1
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Name: 	 	%{name}
Summary: 	Linux Audio Session Handler
Version: 	%{version}
Release: 	%{release}

Source:		http://download.savannah.gnu.org/releases/%name/%{name}-%{version}.tar.gz
URL:		http://www.nongnu.org/lash/
License:	GPLv2+
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gtk2-devel
BuildRequires:	tetex-texi2html
BuildRequires:	jackit-devel libalsa-devel
BuildRequires:	libxml2-devel
BuildRequires:	readline-devel 
BuildRequires:  e2fsprogs-devel
BuildRequires:  ImageMagick
BuildRequires:	python-devel
BuildRequires:	swig
Requires:	python

%description
LASH is a session management system for JACK and ALSA audio applications on
GNU/Linux. Its aim is to allow you to have many different audio programs
running at once, to save their setup, close them down and then easily reload
the setup at some other time. LASH doesn't deal with any kind of audio data
itself; it just runs programs, deals with saving/loading (arbitrary) data and
connects different kinds of virtual audio ports together (currently JACK and
ALSA sequencer ports). It can also be used to move entire sessions between
computers, or post sessions on the Internet for download.

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %name.

%package -n 	%{develname}
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel < %{version}-%{release}
Obsoletes:	%mklibname -d lash 1

%description -n %{develname}
Libraries and includes files for developing programs based on %name.

%package -n	python-%name
Summary:	Python bindings for the LASH audio session handler
Group:		Development/Python
Requires:	%name = %{version}-%{release}

%description -n python-%name
Python bindings for the LASH audio session handler.

%prep
%setup -q
perl -pi -e 's|lib/python|%{_lib}/python||g' configure

%build
%configure2_5x --enable-alsa-midi --enable-debug
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{summary}
Exec=%{_bindir}/%{name}_panel
Icon=%{name}
Terminal=false
Type=Application
Categories=AudioVideo;Audio;AudioVideoEditing;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cp icons/lash_48px.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 icons/lash_96px.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cp icons/lash_16px.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README README.SECURITY TODO
%{_bindir}/*
%{_datadir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*

%files -n python-%name
%defattr(-,root,root)
%{python_sitearch}/*
