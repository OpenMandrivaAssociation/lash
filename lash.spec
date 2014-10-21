%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define badevname %mklibname -d lash 1

Summary:	Linux Audio Session Handler
Name:		lash
Version:	0.5.4
Release:	13
License:	GPLv2+
Group:		Sound
URL:		http://www.nongnu.org/lash/
Source0:	http://download.savannah.gnu.org/releases/%name/%{name}-%{version}.tar.gz
Patch0:		lash-0.5.4-swig2.patch
Patch1:		lash-0.5.4-link.patch
Patch2:		lash-0.5.4-mga-texi2html_Makefile.am.patch
Patch3:		lash-0.5.4-mga-resource.h_lash.c.patch
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	texi2html
BuildRequires:	jackit-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	libxml2-devel
BuildRequires:	readline-devel 
BuildRequires:	libuuid-devel
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(python)
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
Obsoletes:	%{badevname} < %{version}-%{release}

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
%patch0 -p0
%patch1 -p0
%patch2 -p0 -b .lash-0.5.4-mga-texi2html_Makefile.am.patch
%patch3 -p0 -b .lash-0.5.4-mga-resource.h_lash.c.patch

%build
autoreconf -fi -Im4
export CFLAGS="%{optflags} -D_GNU_SOURCE -lm"
export PYTHON=%__python2

%configure \
	--enable-alsa-midi \
	--enable-debug

%make
										
%install
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

find %{buildroot} -name '*.la' -delete

#% find_lang %{name}

%files
# -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README README.SECURITY TODO
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files -n python-%{name}
%{py2_puresitedir}/*
