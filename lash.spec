%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary: 	Linux Audio Session Handler
Name:		lash
Version:	0.5.4
Release:	%mkrel 5
License:	GPLv2+
Group:		Sound
URL:		http://www.nongnu.org/lash/
Source:		http://download.savannah.gnu.org/releases/%name/%{name}-%{version}.tar.gz
BuildRequires:	gtk2-devel
BuildRequires:	tetex-texi2html
BuildRequires:	jackit-devel
BuildRequires:	libalsa-devel
BuildRequires:	libxml2-devel
BuildRequires:	readline-devel 
BuildRequires:	e2fsprogs-devel
BuildRequires:	imagemagick
BuildRequires:	python-devel
BuildRequires:	swig
Requires:	python
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
LASH is a session management system for JACK and ALSA audio applications on
GNU/Linux. Its aim is to allow you to have many different audio programs
running at once, to save their setup, close them down and then easily reload
the setup at some other time. LASH doesn't deal with any kind of audio data
itself; it just runs programs, deals with saving/loading (arbitrary) data and
connects different kinds of virtual audio ports together (currently JACK and
ALSA sequencer ports). It can also be used to move entire sessions between
computers, or post sessions on the Internet for download.

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%{name}-devel < %{version}-%{release}
Obsoletes:	%mklibname -d lash 1

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.

%package -n python-%{name}
Summary:	Python bindings for the LASH audio session handler
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-%{name}
Python bindings for the LASH audio session handler.

%prep
%setup -q
perl -pi -e 's|lib/python|%{_lib}/python||g' configure

%build
export CFLAGS="%{optflags} -D_GNU_SOURCE"

%configure2_5x \
	--enable-alsa-midi \
	--enable-debug

%make
										
%install
rm -rf %{buildroot}
%makeinstall_std

#menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
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
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
cp icons/lash_48px.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -size 32x32 icons/lash_96px.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
cp icons/lash_16px.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README README.SECURITY TODO
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*

%files -n python-%{name}
%defattr(-,root,root)
%{python_sitelib}/*
