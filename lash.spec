%define	major		1
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d

Summary:		Linux Audio Session Handler
Name:		lash
Version:		0.5.4
Release:		10
License:		GPLv2+
Group:		Sound
URL:		http://www.nongnu.org/lash/
Source0:		http://download.savannah.gnu.org/releases/%name/%{name}-%{version}.tar.gz
BuildRequires:	gtk2-devel >= 2.0.0
BuildRequires:	texi2html
BuildRequires:	jackit-devel >= 0.99.17
BuildRequires:	libalsa-devel >= 0.9
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	readline-devel 
BuildRequires:	libuuid-devel
BuildRequires:	imagemagick
BuildRequires:	python-devel
BuildRequires:	swig
Requires:	python

%description
LASH is a session management system for JACK and ALSA audio applications on
GNU/Linux. Its aim is to allow you to have many different audio programs
running at once, to save their setup, close them down and then easily
reload the setup at some other time. LASH doesn't deal with any kind of
audio data itself; it just runs programs, deals with saving/loading
(arbitrary) data and connects different kinds of virtual audio ports
together (currently JACK and ALSA sequencer ports). It can also be used to
move entire sessions between computers, or post sessions on the Internet
for download.


%package -n %{libname}
Summary:		Dynamic libraries from %{name}
Group:		System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.


%package -n %{develname}
Summary:		Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%{name}-devel < %{version}-%{release}
Obsoletes:	%{_lib}lash1-devel < %{version}-%{release}

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.

# (gvm) configure.ac has the building of python bindings always disabled
# so this package will be empty
#%%package -n python-%%{name}
#Summary:		Python bindings for the LASH audio session handler
#Group:		Development/Python
#Requires:	%{name} = %{version}-%{release}

#description -n python-%%{name}
#Python bindings for the LASH audio session handler.


%prep
%setup -q

perl -pi -e 's|lib/python|%{_lib}/python||g' configure


%build
export CFLAGS="%{optflags} -D_GNU_SOURCE"
export LIBS="-lpthread -luuid -lm"
%configure2_5x \
	--enable-alsa-midi \
	--enable-debug
%make


%install
%makeinstall_std

# Drop .la archives
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;

# Make sure the libraries are executables
chmod 0755 %{buildroot}%{_libdir}/lib*.so.*

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


%files
%doc AUTHORS ChangeLog NEWS README README.SECURITY TODO
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png


%files -n %{libname}
%doc README
%{_libdir}/*.so.%{major}*


%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
#{_libdir}/*.la
%{_libdir}/pkgconfig/*


#files -n python-%%{name}
#%%{python_sitelib}/*


%changelog
* Wed Oct 31 2012 Giovanni Mariani <mc2374@mclink.it> 0.5.4-10
- Dropped BuildRoot, %%mkrel, %%defattr and %%clean section
- Dropped support for ancient distro releases
- Dropped python-lash package, because the building of the python bindings
  now is disabled in the sources
- Fixed linking with libpthread and libuuid
- Added some version info to BReqs, according to the configure output
- Made sure that Description text lines are < 76 chars in lenght
- Made rpmlint more happy and killed some warnings
- Removed .la files

* Mon Feb 22 2010 Funda Wang <fwang@mandriva.org> 0.5.4-9mdv2010.1
+ Revision: 509779
- BR uuid
  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.4-8mdv2009.1
+ Revision: 354772
- rebuild

* Tue Mar 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.4-7mdv2009.1
+ Revision: 348118
- disable parallel build
- rebuild for latest readline

* Sat Jan 03 2009 Funda Wang <fwang@mandriva.org> 0.5.4-6mdv2009.1
+ Revision: 323755
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Mon Aug 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.5.4-5mdv2009.0
+ Revision: 270767
- remove stupid redefines
- fix mixture of tabs and spaces
- export -D_GNU_SOURCE to make it build
- put icons into fd.o directories
- spec file clean

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 14 2007 Funda Wang <fwang@mandriva.org> 0.5.4-2mdv2008.1
+ Revision: 119657
- revert to python_sitelib
- New version 0.5.4
- drop old menu
- new devel policy

  + Thierry Vignaud <tv@mandriva.org>
    - fix summary-ended-with-dot
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Austin Acton <austin@mandriva.org>
    - increase release
    - even better python libdir hack
    - buildrequires swig
    - split off python package
    - move python_sitelib files to python_sitearch
    - new version
    - force midi
    - major 1.1 and epoch 1 (weird)
    - require python
    - remove info page


* Tue Sep 05 2006 Emmanuel Andry <eandry@mandriva.org> 0.5.0-2mdv2007.0
- disable gtk1.2
- xdg menu

* Sun Feb 19 2006 Austin Acton <austin@mandriva.org> 0.5.0-1mdk
- initial package

