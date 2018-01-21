%define commit 94b2bf2a183e72a0ea68e3a86538d32d9a596889
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%define filter_name captdriver
%define date 20170216

Summary:	Cups filter for Canon CAPT printers
Name:		cups-drivers-%{filter_name}
Version:	0_git%{date}
Release:	0
License:	GPLv3+
Group:		System/Printing
Url:		https://github.com/agalakhov/captdriver
#Source0:	https://github.com/agalakhov/%{filter_name}/archive/%{filter_name}-%{version}.tar.gz
Source0:	https://github.com/agalakhov/%{filter_name}/archive/%{commit}/%{filter_name}-%{commit}.zip
# https://sourceforge.net/p/foo2capt/foo2capt/ci/master/tree/capt.drv?format=raw
Source1:	capt.drv

BuildRequires:	cups
BuildRequires:	cups-common
BuildRequires:	cups-devel

%description
This is a driver for Canon CAPT-based printers (LBP-***)
based on several reverse engineering attempts. This is
currently in an early alpha stage. Use at your own risk.

Actually it supports the following models:
  * LBP2900 (works)
  * LBP3000 (experimental)
  * LBP3010 (experimental)
  * LBP3018 (experimental)
  * LBP3050 (experimental)

%files
%{_libdir}/cups/filter/rastertocapt
%{_datadir}/cups/model/%{filter_name}/*ppd
%doc README
%doc SPECS
#doc NEWS
#doc ChangeLog
%doc AUTHORS
%doc COPYING

#----------------------------------------------------------------------------

%prep
%setup -qn %{filter_name}-%{commit}

# Create a different PPD file for each supported model LBP-3010
ppdc %{SOURCE1}

%build
autoreconf -fiv
%configure
%make

%install
#% makeinstall_std

# filter
install -dm 0755 %{buildroot}%{_libdir}/cups/filter/
install -pm 0755 src/rastertocapt %{buildroot}%{_libdir}/cups/filter/

# PPD files
install -dm 0755 %{buildroot}%{_datadir}/cups/model/%{filter_name}/
#install -pm 0644 Canon-LBP-*.ppd %{buildroot}%{_datadir}/cups/model/%{filter_name}/
for m in 2900 3000 3010 3018 3050
do
  install -pm 644 Canon-LBP-${m}.ppd %{buildroot}%{_datadir}/cups/model/%{filter_name}/
done

