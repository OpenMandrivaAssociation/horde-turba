%define	module	turba
%define __noautoreq /usr/bin/php

Name: 		horde-%{module}
Version: 	2.3.6
Release: 	4
Summary:	The Horde contact manager

License:	LGPL
Group:		System/Servers
Source:		ftp://ftp.horde.org:21/pub/turba/turba-h3-%{version}.tar.gz
URL:		https://www.horde.org/%{module}/
Requires(post):	rpm-helper
Requires:	horde >= 3.3.5
Requires:	php-pear-Net_LDAP
BuildArch:	noarch

%description
Turba is the Horde contact management application, which allows access
to and storage of personal contacts (including name, email address,
phone number, and other easily customizable fields). Turba integrates
with IMP (Horde's webmail application) as its address book.

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Require all denied
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Turba Horde configuration file
//
 
$this->applications['turba'] = array(
    'fileroot'    => $this->applications['horde']['fileroot'] . '/turba',
    'webroot'     => $this->applications['horde']['webroot'] . '/turba',
    'name'        => _("Address Book"),
    'status'      => 'active',
    'provides'    => array('contacts', 'clients'),
    'menu_parent' => 'organizing'
);
EOF
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR js %{buildroot}%{_datadir}/horde/%{module}
cp -pR addressbooks %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

# fix script shellbang
for file in `find %{buildroot}%{_datadir}/horde/%{module}/scripts`; do
	perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|' $file
done

# additional cleanup
rm -f %{buildroot}%{_datadir}/horde/%{module}/scripts/Turba.reg


%post
if [ $1 = 1 ]; then
	# generate configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi

%files
%doc README LICENSE docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


