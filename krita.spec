%define _python_bytecompile_errors_terminate_build 0

%define stable %([ -n "%{?beta:%{beta}}" ] && echo -n un; echo -n stable)
# See rpmlintrc for reason
%define __requires_exclude 'devel.*'
#define _disable_lto 1

Name: krita
Version: 5.1.2
Release: 1
Source0: http://download.kde.org/stable/krita/%(echo %{version} |cut -d. -f1-3)/%{name}-%{version}%{?beta:%{beta}}.tar.xz
# The krita plugin requires a patched version of gmic
Source1: https://github.com/amyspark/gmic/releases/download/v3.1.5.1/gmic-3.1.5.1-patched.tar.xz
Source1000: %{name}.rpmlintrc
#ifarch %{arm} %{armx}
#Patch0:	krita-4.4.2-OpenMandriva-fix-build-with-OpenGLES-aarch64-and-armvhnl.patch
#endif
# Fix build with SSE
#Patch2: krita-4.4.8-sse-compile.patch
Patch3: krita-5.0.0-fix-libatomic-linkage.patch
# And make it compile
Patch5: krita-5.0.2-gmic-compile.patch

#Upstream patch
#Patch10:	4523-Support-building-with-OpenEXR-3.patch

Summary: Sketching and painting program
URL: http://krita.org/
License: GPL
Group: Graphics
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5PrintSupport)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Sql)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5QuickWidgets)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF5Archive)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5WidgetsAddons)
BuildRequires: cmake(KF5Completion)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: cmake(KF5GuiAddons)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5ItemModels)
BuildRequires: cmake(KF5ItemViews)
BuildRequires: cmake(KF5WindowSystem)
BuildRequires: cmake(KF5KIO)
BuildRequires: cmake(KF5Crash)
#BuildRequires: cmake(KSeExpr)
# FIXME figure out why -- doesn't look like anything is
# actually insane enough to link libjpeg statically
BuildRequires: jpeg-static-devel
BuildRequires: cmake(QuaZip-Qt5)
# x86 package
%ifarch %{ix86} %{x86_64}
BuildRequires: cmake(Vc)
%endif
BuildRequires: boost-devel
BuildRequires: %{_lib}atomic-devel
BuildRequires: pkgconfig(python)
BuildRequires: pkgconfig(eigen3)
BuildRequires: pkgconfig(exiv2)
BuildRequires: pkgconfig(fftw3)
BuildRequires: pkgconfig(gsl)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(libraw)
BuildRequires: pkgconfig(libraw_r)
BuildRequires: pkgconfig(shared-mime-info)
# Krita in 4.4.X is not compatibile with OpenColorIO v2.
# Version 5.0.0 beta1 add support for compiling with OCIO v2 but still not runtime. Need wait for another beta.
# Until then, we use compat package with OpenColorIO v1 to allow compiling current 4.4.8 Krita.
# Please do not backport Krita or OCIO to Lx 4.2 or Rolling.
%ifnarch %{armx}
BuildRequires: pkgconfig(OpenColorIO) >= 2
%endif
BuildRequires: pkgconfig(poppler-qt5)
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(zlib)
# for gmic
BuildRequires: pkgconfig(libavcodec)
BuildRequires: atomic-devel
# Optional -- for EXR file format support
BuildRequires: pkgconfig(OpenEXR) >= 3.0.0
BuildRequires: pkgconfig(gsl)
BuildRequires: giflib-devel
BuildRequires: python-qt5-devel
BuildRequires: python-qt5-core
BuildRequires: python-qt5-gui
BuildRequires: python-qt5-widgets
BuildRequires: python-qt5-xml
BuildRequires: python-sip
Requires: python-qt5-xml

# Those used to be separate libpackages in 2.x, but it didn't make much
# sense, nothing outside of krita uses those libraries (and nothing can,
# they don't come with headers...)
Obsoletes: calligra-krita < %{EVRD}
Obsoletes: %{_lib}kritacolord < %{EVRD}
Obsoletes: %{_lib}kritacolor14 < %{EVRD}
Obsoletes: %{_lib}kritalibpaintop14 < %{EVRD}
Obsoletes: %{_lib}kritaui14 < %{EVRD}
# This used to be part of gmic, it's now part of krita
%rename krita-plugin-gmic

%define langlist af ar ast be bg br bs ca cs cy da de el en_GB eo es et eu fa fi fr fy ga gl he hi hne hr hu ia is it ja kk km ko lt lv mai mk mr ms nb nds ne nl nn oc pa pl pt pt_BR ro ru se sk sl sq sv ta tg th tr ug uk uz vi wa xh zh_CN zh_TW

%{expand:%(for lang in %langlist; do echo "Obsoletes:	krita-l10n-$lang"; done)}

%description
Krita offers an end–to–end solution for creating digital painting files
from scratch by masters. It supports concept art, creation of comics
and textures for rendering.

%prep
%autosetup -p1 -n %{name}-%{version}%{?beta:%{beta}}
%cmake_kde5 \
	-DUSE_QT_XCB:BOOL=TRUE \
	-DENABLE_BSYMBOLICFUNCTIONS:BOOL=TRUE \
	-G Ninja

%build
%ifarch %{arm} %{armx}
export CXXFLAGS="%{optflags} -DHAS_ONLY_OPENGL_ES"
%endif
%ninja -C build -w dupbuild=warn

%install
%ninja_install -C build -w dupbuild=warn

# Not very nice to do additional builds here, but
# the gmic plugin requires a krita installation in
# a buildroot to locate headers etc.
mkdir build-plugins
cd build-plugins
cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=TRUE \
	-DEXTERNALS_DOWNLOAD_DIR=%{_sourcedir} \
	-DINSTALL_ROOT=%{buildroot}%{_prefix} \
	-G Ninja \
	../3rdparty_plugins
%ninja_build
cd -

# We get those from breeze...
rm -f %{buildroot}%{_datadir}/color-schemes/Breeze*.colors
# Currently nothing uses Krita headers, so we don't need them
rm -rf %{buildroot}%{_includedir}
# This isn't an AppImage, so we don't need the update dummy
rm -f %{buildroot}%{_bindir}/AppImageUpdateDummy

%find_lang krita || touch krita.lang

%files -f krita.lang
%config %{_sysconfdir}/xdg/kritarc
%{_bindir}/krita
%{_bindir}/kritarunner
%{_bindir}/krita_version
%{_datadir}/metainfo/org.kde.krita.appdata.xml
%{_datadir}/applications/*
%{_libdir}/libkrita*.so*
%{_libdir}/krita-python-libs/
%dir %{_libdir}/kritaplugins
%{_libdir}/kritaplugins/*.so
%{_libdir}/qt5/qml/org/krita
%{_iconsdir}/hicolor/*x*/apps/krita.png
%{_iconsdir}/hicolor/scalable/apps/krita.svgz
%{_datadir}/icons/*/*/*/application-x-krita.*
%{_datadir}/%{name}
%{_datadir}/kritaplugins
%{_datadir}/color/icc/krita
%{_datadir}/color-schemes/Krita*.colors
%{_datadir}/gmic
