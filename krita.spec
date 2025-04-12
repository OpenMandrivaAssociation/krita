%define _python_bytecompile_errors_terminate_build 0

%define stable %([ -n "%{?beta:%{beta}}" ] && echo -n un; echo -n stable)
# See rpmlintrc for reason
%define __requires_exclude 'devel.*'
#define _disable_lto 1

# Need to fix a few downloaded external dependencies first
%bcond_with aitools

Name: krita
Version: 5.2.9
Release: 4
#Source0: http://download.kde.org/stable/krita/%(echo %{version} |cut -d. -f1-3)/%{name}-%{version}%{?beta:%{beta}}.tar.xz
Source0: https://invent.kde.org/graphics/krita/-/archive/v%{version}/krita-v%{version}.tar.bz2
# The krita plugin requires a patched version of gmic
# git repo: https://github.com/amyspark/gmic
# Make sure the version (and filename!) always matches what's requested in
# 3rdparty_plugins/ext_gmic/CMakeLists.txt
Source1: https://files.kde.org/krita/build/dependencies/gmic-3.5.0.1-patched.tar.gz
%if %{with aitools}
# AI selection plugin, see https://github.com/Acly/krita-ai-tools
Source2: https://github.com/Acly/krita-ai-tools/archive/refs/tags/v1.0.2.tar.gz
Source3: https://github.com/Acly/dlimgedit/archive/refs/heads/main.tar.gz
%endif
Source1000: %{name}.rpmlintrc
#ifarch %{arm} %{armx}
#Patch0:	krita-4.4.2-OpenMandriva-fix-build-with-OpenGLES-aarch64-and-armvhnl.patch
#endif
Patch1: krita-5.2.3-xsimd-compile.patch
# Fix build with SSE
#Patch2: krita-4.4.8-sse-compile.patch
Patch3: krita-5.0.0-fix-libatomic-linkage.patch
# And make it compile
Patch4: krita-dont-hardcode-ancient-sip-abi.patch
Patch5: krita-5.0.2-gmic-compile.patch
# This is needed because discover (as of 5.27.6) barfs on tags inside <caption>
# It should be removed if and when discover can deal with links inside caption.
#Patch6: metadata-no-links.patch
%if %{with aitools}
# Fix krita-ai-tools build...
Patch7: krita-ai-tools-dont-download-dlimgedit.patch
# ... and installation
Patch8: krita-ai-tools-install-dirs.patch
%endif
Patch9: krita-5.2.9-open-avif-through-qimageio.patch

#Upstream patch
#Patch10:	4523-Support-building-with-OpenEXR-3.patch

Summary: Sketching and painting program
URL: https://krita.org/
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
BuildRequires: cmake(Qt5LinguistTools)
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
BuildRequires: cmake(KF5KDcraw)
BuildRequires: cmake(Mlt7)
BuildRequires: cmake(SDL2)
BuildRequires: pkgconfig(libwebp)
#BuildRequires: cmake(KSeExpr)
# FIXME figure out why -- doesn't look like anything is
# actually insane enough to link libjpeg statically
BuildRequires: jpeg-static-devel
BuildRequires: cmake(QuaZip-Qt5)
# x86 package
%ifarch %{ix86} %{x86_64}
BuildRequires: cmake(Vc)
%endif
BuildRequires: cmake(Immer)
BuildRequires: %mklibname -d zug
BuildRequires: %mklibname -d lager
BuildRequires: cmake(xsimd)
BuildRequires: boost-devel
BuildRequires: pkgconfig(libunibreak)
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
BuildRequires: pkgconfig(libjxl)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(libraw)
BuildRequires: pkgconfig(libraw_r)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(fribidi)
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
BuildRequires: pkgconfig(libmypaint)
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
Requires: qt5-database-plugin-sqlite
Requires: python-qt5-core
Requires: python-qt5-gui
Requires: python-qt5-widgets
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
%setup -q -n %{name}-v%{version}%{?beta:%{beta}}
%if %{with aitools}
cd plugins
tar xf %{S:2}
mv krita-ai-tools-* krita-ai-tools
echo 'add_subdirectory(krita-ai-tools)' >>CMakeLists.txt
cd krita-ai-tools
tar xf %{S:3}
mv dlimgedit-* dlimgedit
sed -i -e '/fmt/d' dlimgedit/CMakeLists.txt
cd ../..
%endif
%autopatch -p1

%cmake_kde5 \
	-DUSE_QT_XCB:BOOL=TRUE \
	-DENABLE_BSYMBOLICFUNCTIONS:BOOL=TRUE \
	-DPC_xsimd_CONFIG_DIR=%{_libdir}/cmake/xsimd \
	-G Ninja

%build
%ifarch %{arm} %{armx}
export CXXFLAGS="%{optflags} -DHAS_ONLY_OPENGL_ES"
%endif
%ninja -C build

%install
%ninja_install -C build

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
	-DPC_xsimd_CONFIG_DIR=%{_libdir}/cmake/xsimd \
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
%{_iconsdir}/hicolor/*x*/apps/krita.png
%{_iconsdir}/hicolor/scalable/apps/krita.svgz
%{_datadir}/icons/*/*/*/application-x-krita.*
%{_datadir}/%{name}
%{_datadir}/kritaplugins
%{_datadir}/color/icc/krita
%{_datadir}/color-schemes/Krita*.colors
%{_datadir}/gmic
