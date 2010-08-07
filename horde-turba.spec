%define	module	turba
%define	name	horde-%{module}
%define version 2.3.4
%define release %mkrel 1
%define _requires_exceptions pear(.*)

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	The Horde contact manager
License:	LGPL
Group:		System/Servers
Source:		ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
URL:		http://www.horde.org/%{module}/
Requires(post):	rpm-helper
Requires:	horde >= 3.3.5
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
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
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


%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# generate configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc README LICENSE docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
