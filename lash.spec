%define name	lash
%define version	0.5.0
%define release %mkrel 3

%define major	2
%define libname %mklibname %name %major

Name: 	 	%{name}
Summary: 	Linux Audio Session Handler
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
URL:		http://www.nongnu.org/lash/
License:	GPL
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gtk2-devel
BuildRequires:	tetex-texi2html
BuildRequires:	jackit-devel libalsa-devel
BuildRequires:	libxml2-devel
BuildRequires:	readline-devel 
BuildRequires:  e2fsprogs-devel
BuildRequires:  ImageMagick

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

%package -n 	%{libname}-devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep
%setup -q

%build
%configure2_5x --enable-gtk2 --disable-gtk --disable-serv-inst
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="lash_panel" icon="%{name}.png" needs="x11" title="LASH Control Panel" longtitle="Audio session manager" section="Multimedia/Sound" xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{summary}
Exec=%{_bindir}/%{name}_panel
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;AudioVideo;Audio;
Encoding=UTF-8
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
%_install_info %{name}-manual.info
		
%preun
%_remove_install_info %{name}-manual.info

%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README README.SECURITY TODO
%{_bindir}/*
%{_datadir}/%name
%{_menudir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%{_infodir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*



