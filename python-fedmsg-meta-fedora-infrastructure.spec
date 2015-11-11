#
# Conditional build:
%bcond_with	tests	# do not perform "make test"

%define 	module	fedmsg_meta_fedora_infrastructure
Summary:	Metadata providers for Fedora Infrastructure's fedmsg deployment
Name:		python-fedmsg-meta-fedora-infrastructure
Version:	0.15.4
Release:	0.1
License:	LGPL v2+
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/f/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	a76cc29b3205815cc44fbd1beae17564
URL:		http://pypi.python.org/pypi/fedmsg_meta_fedora_infrastructure
BuildRequires:	fedmsg >= 0.10.0
BuildRequires:	python-dateutil
#BuildRequires:	python-fedora
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	fedmsg >= 0.7.7
Requires:	python-dateutil
#Requires:	python-fedora
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Metadata providers for Fedora Infrastructure's fedmsg deployment

fedmsg <http://fedmsg.com> is a set of tools for knitting together
services and webapps into a realtime messaging net. This package
contains metadata provider plugins for the primary deployment of that
system: Fedora Infrastructure
<http://fedoraproject.org/wiki/Infrastructure>.

If you were to deploy fedmsg at another site, you would like want to
write your own module like this one that could provide textual
representations of your messages.

%prep
%setup -q -n %{module}-%{version}

# Remove bundled egg-info in case it exists
rm -r %{module}.egg-info

%build
%{__python} setup.py build

%if %{with tests}
# Go ahead and run tests for fedora and friends
PYTHONPATH=. FEDMSG_META_NO_NETWORK=True nosetests
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/fedmsg_meta_fedora_infrastructure/tests

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%dir %{py_sitescriptdir}/fedmsg_meta_fedora_infrastructure
%{py_sitescriptdir}/fedmsg_meta_fedora_infrastructure/*.py[co]
%{py_sitescriptdir}/fedmsg_meta_fedora_infrastructure/conglomerators
%{py_sitescriptdir}/fedmsg_meta_fedora_infrastructure-%{version}-py*.egg-info
