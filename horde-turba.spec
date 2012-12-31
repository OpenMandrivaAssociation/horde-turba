%define	module	turba
%define	name	horde-%{module}

Name: 		%{name}
Version: 	2.3.6
Release: 	1
Summary:	The Horde contact manager
License:	LGPL
Group:		System/Servers
Source:		ftp://ftp.horde.org:21/pub/turba/turba-h3-%{version}.tar.gz
URL:		http://www.horde.org/%{module}/
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


%post
if [ $1 = 1 ]; then
	# generate configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi

%files
%defattr(-,root,root)
%doc README LICENSE docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Wed Mar 30 2011 Adam Williamson <awilliamson@mandriva.org> 2.3.5-1mdv2011.0
+ Revision: 648802
- new release 2.3.5

* Sun Aug 29 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.3.4-2mdv2011.0
+ Revision: 574210
- added requires php-pear-Net_LDAP

* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.3.4-1mdv2011.0
+ Revision: 567528
- Updated to version 2.3.4
- added version 2.3.4 source file

* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.3.2-5mdv2011.0
+ Revision: 565222
- Increased release for rebuild
- Increased release for rebuild
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.2-4mdv2010.1
+ Revision: 493352
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.2-2mdv2010.0
+ Revision: 445913
- don't forget call webapps post-installation macros to load module configuration

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.2-1mdv2010.0
+ Revision: 445890
- raise horde version dependency
- new version
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 2.3.1-2mdv2010.0
+ Revision: 437887
- rebuild

* Sun Dec 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.1-1mdv2009.1
+ Revision: 314344
- update to new version 2.3.1

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.3-1mdv2009.1
+ Revision: 295280
- update to new version 2.3

* Wed Jun 25 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.1-1mdv2009.0
+ Revision: 228895
- new version

* Tue Jun 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2-3mdv2009.0
+ Revision: 223593
- add missing js and addressbooks directories (fix #41531)

* Fri May 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2-2mdv2009.0
+ Revision: 213373
- don't duplicate spec-helper work
- update to new version 2.2

* Wed Jan 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.6-1mdv2008.1
+ Revision: 153780
- update to new version 2.1.6

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.5-1mdv2008.1
+ Revision: 133741
- update to new version 2.1.5

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Sep 06 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.4-1mdv2008.0
+ Revision: 81208
- update to new version 2.1.4


* Mon Dec 18 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.3-1mdv2007.0
+ Revision: 98598
- new version
  use herein document for horde configuration

  + Andreas Hasenack <andreas@mandriva.com>
    - Import horde-turba

* Sat Aug 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.2-2mdv2007.0
- Rebuild

* Sat Aug 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.2-1mdv2007.0
- New version 2.1.2

* Tue May 23 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.1-1mdk
- New release 2.1.1

* Tue Mar 07 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-1mdk
- new version

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.5-1mdk
- New release 2.0.5

* Sat Sep 17 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.3-2mdk 
- explicit dependency exception, as all those modules are provided by horde itself 
- %%mkrel

* Sat Aug 20 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.3-1mdk
- New release 2.0.3
- better fix encoding

* Fri Jul 01 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.2-2mdk 
- better fix encoding
- fix requires
- no automatic config generation, incorrect default values
- horde isn't a prereq
- spec cleanup

* Sun Apr 17 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0.2-1mdk
- New release 2.0.2

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0-3mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Mon Jan 17 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-2mdk
- fix inclusion path
- fix configuration perms
- generate configuration at postinstall
- horde and rpm-helper are now a prereq

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-1mdk 
- new version
- top-level is now /var/www/horde/turba
- config is now in /etc/horde/turba
- other non-accessible files are now in /usr/share/horde/turba
- drop safemode build
- drop old obsoletes
- drop all patches
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Tue Jul 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.2-3mdk 
- apache config file in /etc/httpd/webapps.d

* Sun May 02 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.2-2mdk
- renamed to horde-turba
- pluggable horde configuration
- standard perms for /etc/httpd/conf.d/%%{order}_horde-turba.conf
- don't provide useless ADVXpackage virtual package
- remove redundant requires, as horde already requires them

* Tue Apr 06 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.2-1mdk
- new version

* Sat Dec 20 2003 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.1-2mdk
- untagged localisation files
- no more .htaccess files, use /etc/httpd/conf.d/%%{order}_turba.conf instead
- scripts now in  /usr/share/{name}


