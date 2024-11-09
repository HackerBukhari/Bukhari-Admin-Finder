import requests
from urllib.parse import urljoin
import time

# Common admin paths
admin_paths = [
    "/admin",
    "/administrator",
    "/admin/login",
    "/admin/index.php",
    "/wp-admin",
    "/admin_area",
    "/backend",
    "/login",
    "/adminpanel"
    '/wp-admin/', '/wp-login.php', '/wp-login', '/wp-admin.php', '/wp-login-form',

    # Joomla
    '/administrator', '/administrator/index.php', '/administrator/login', '/administrator/admin-login',

    # Drupal
    '/user/login/', '/admin/', '/admin/login/', '/user/logout/', '/user/admin/', '/admin/login-form/', '/admin-area/',

    # Magento
    '/admin', '/admin/dashboard', '/adminpanel', '/admin-login/', '/admin_area/', '/manager', '/adminlogin', '/admin/control',

    # PrestaShop
    '/admin', '/adminlogin.php', '/admin_area/', '/adminpanel',

    # OpenCart
    '/admin', '/adminpanel', '/admin/config.php', '/adminlogin.php',

    # TYPO3
    '/typo3', '/typo3/login.php', '/typo3/typo3/', '/typo3/backend/', '/backend/',

    # Bitrix
    '/bitrix', '/bitrix/admin', '/bitrix/admin_panel', '/bitrix/login.php', '/admin/bitrix',

    # Shopify
    '/admin', '/admin/login', '/admin/login.php', '/admin-area', '/admin/dashboard',

    # Laravel (Custom / Artisan Routes)
    '/admin', '/admin/login', '/admin/dashboard', '/admin/auth', '/adminpanel', '/login', '/controlpanel',

    # Open Source Platforms (Custom CMS)
    '/panel', '/admin_area', '/admin-console', '/secure-admin', '/adminform', '/admin-login', '/administrator-login',

    # Common paths
    '/admin/', '/administrator/', '/admin1/', '/admin2/', '/admin3/', '/adminpanel/', '/cpanel/', '/controlpanel/', '/manage/', 
    '/manage_admin/', '/adminlogin/', '/admin_area/', '/adminhome/', '/admin_dashboard/', '/administrator_login/', '/dashboard/', 
    '/loginadmin/', '/adminlogin.php', '/login.php', '/login.asp', '/admin_login.php', '/admin/index.php', '/index.php', '/admin_home.php',
    
    # CMS-specific paths
    '/wp-admin/', '/wp-login.php', '/wp-login/', '/wp-admin/admin.php', '/admin-login.php', '/admin-dashboard/', '/administratorcp/', 
    '/typo3/', '/joomla/', '/drupal/', '/magento/', '/opencart/', '/cmsadmin/', '/cms-login/', '/cms-admin/', '/joomla_login/', 
    '/joomla-admin/', '/joomla-backend/', '/joomla_adm/', '/admin_console/', '/back-end/', '/backoffice/', '/cpanel-admin/', 
    '/adminpanel.php', '/wp-admin/login.php', '/wp-admin-dashboard/', '/wp-login-admin/', '/wp-login-panel/', '/adminwp.php',
    
    # Web app and general admin panel paths
    '/backend/', '/secureadmin/', '/secure_login/', '/admin_secure/', '/admintool/', '/admin_area/login.php', '/admin_area/index.php',
    '/admin/login/', '/backend/admin/', '/admincp/', '/cms-admin/login.php', '/console/', '/panel/', '/adminpage/', '/adminsignon/',
    '/admin/index.html', '/admin_home.html', '/adminarea.html', '/adminlogin.html', '/admin_login/', '/superadmin/', '/admincp.html',
    
    # Specific software paths
    '/adminer.php', '/adminpanel2/', '/adminarea.php', '/siteadmin/', '/manager/', '/dologin.php', '/useradmin/', '/sysadmin/', 
    '/adminauth.php', '/management/', '/adminconfig/', '/panel-adm/', '/admin_panel/', '/secure/', '/webadmin/', '/sysadmin_login/',
    
    # Uncommon/Obscure paths
    '/superuser/', '/admincontrol/', '/rootadmin/', '/systemadmin/', '/websysadmin/', '/dmin/', '/webconfig/', '/confadmin/',
    '/admincenter/', '/admin_dashboard.php', '/admin-console.php', '/adminsetting.php', '/admin_forms/', '/adminserver/', '/adminb/',
    '/adminindex.php', '/admintoolbox/', '/backofficeadmin/', '/webadmintool/', '/admin-panel/', '/web_admin/', '/manager_login/',
    
    # Other possibilities
    '/management_login/', '/admin_user/', '/admin-setup/', '/admin-controls/', '/web-login/', '/admintools/', '/admin_update/', 
    '/admin_settings.php', '/admin-config/', '/admin/addnewuser.php', '/login_admin/', '/adminenter/', '/admins_login/', 
    '/administrator_auth/', '/admin/signin/', '/admindashboard/', '/admin_settings/', '/admin_tools/', '/administration_tools/', 
    '/admin-actions/', '/admin_login_action/', '/admin_check/', '/admin_access.php', '/sysadmin_dashboard/', '/admin_tools.php',
    '/admin/settings.php', '/admin/settings', '/adminauth/', '/system-config/', '/root-admin/', '/master-admin/', '/admin_home/', 
    '/adminpanel2.php', '/adminconfig.php'    
    '/acceso.asp', '/acceso.php', '/access/', '/access.php', '/account/', '/account.asp', '/account.html', '/account.php', 
    '/acct_login/', '/_adm_/', '/adm/', '/adm2/', '/adm/admloginuser.asp', '/adm/admloginuser.php', '/adm.asp', '/adm_auth.asp', 
    '/adm_auth.php', '/adm.html', '/_admin_/', '/admin/', '/Admin/', '/ADMIN/', '/admin1/', '/admin1.asp', '/admin1.html', 
    '/admin1.php', '/admin2/', '/admin2.asp', '/admin2.html', '/admin2/index/', '/admin2/index.asp', '/admin2/index.php', 
    '/admin2/login.asp', '/admin2/login.php', '/admin2.php', '/admin3/', '/admin4/', '/admin4_account/', '/admin4_colon/', 
    '/admin5/', '/admin/account.asp', '/admin/account.html', '/admin/account.php', '/admin/add_banner.php/', '/admin/addblog.php', 
    '/admin/add_gallery_image.php', '/admin/add.php', '/admin/add-room.php', '/admin/add-slider.php', '/admin/add_testimonials.php', 
    '/admin/admin/', '/admin/adminarea.php', '/admin/admin.asp', '/admin/AdminDashboard.php', '/admin/admin-home.php', 
    '/admin/AdminHome.php', '/admin/admin.html', '/admin/admin_index.php', '/admin/admin_login.asp', '/admin/admin-login.asp', 
    '/admin/adminLogin.asp', '/admin/admin_login.html', '/admin/admin-login.html', '/admin/adminLogin.html', '/admin/admin_login.php', 
    '/admin/admin-login.php', '/admin/adminLogin.php', '/admin/admin_management.php', '/admin/admin.php', '/admin/admin_users.php', 
    '/admin/adminview.php', '/admin/adm.php', '/admin_area/', '/adminarea/', '/admin_area/admin.asp', '/adminarea/admin.asp', 
    '/admin_area/admin.html', '/adminarea/admin.html', '/admin_area/admin.php', '/adminarea/admin.php', '/admin_area/index.asp', 
    '/adminarea/index.asp', '/admin_area/index.html', '/adminarea/index.html', '/admin_area/index.php', '/adminarea/index.php', 
    '/admin_area/login.asp', '/adminarea/login.asp', '/admin_area/login.html', '/adminarea/login.html', '/admin_area/login.php', 
    '/adminarea/login.php', '/admin.asp', '/admin/banner.php', '/admin/banners_report.php', '/admin/category.php', '/admin/change_gallery.php', 
    '/admin/checklogin.php', '/admin/configration.php', '/admincontrol.asp', '/admincontrol.html', '/admincontrol/login.asp', 
    '/admincontrol/login.html', '/admincontrol/login.php', '/admin/control_pages/admin_home.php', '/admin/controlpanel.asp', 
    '/admin/controlpanel.html', '/admin/controlpanel.php', '/admincontrol.php', '/admincontrol.php/', '/admin/cpanel.php', 
    '/admin/cp.asp', '/admin/CPhome.php', '/admin/cp.html', '/admincp/index.asp', '/admincp/index.html', '/admincp/login.asp', 
    '/admin/cp.php', '/admin/dashboard/index.php', '/admin/dashboard.php', '/admin/dashbord.php', '/admin/dash.php', '/admin/default.php', 
    '/adm/index.asp', '/adm/index.html', '/adm/index.php', '/admin/enter.php', '/admin/event.php', '/admin/form.php', '/admin/gallery.php', 
    '/admin/headline.php', '/admin/home.asp', '/admin/home.html', '/admin_home.php', '/admin/home.php', '/admin.html', '/admin/index.asp', 
    '/admin/index-digital.php', '/admin/index.html', '/admin/index.php', '/admin/index_ref.php', '/admin/initialadmin.php', '/administer/', 
    '/administr8/', '/administr8.asp', '/administr8.html', '/administr8.php', '/administracion.php', '/administrador/', '/administratie/', 
    '/administration/', '/administration.html', '/administration.php', '/administrator', '/_administrator_/', '/_administrator/', '/administrator/', 
    '/administrator/account.asp', '/administrator/account.html', '/administrator/account.php', '/administratoraccounts/', '/administrator.asp', 
    '/administrator.html', '/administrator/index.asp', '/administrator/index.html', '/administrator/index.php', '/administratorlogin/', 
    '/administrator/login.asp', '/administratorlogin.asp', '/administrator/login.html', '/administrator/login.php', '/administratorlogin.php', 
    '/administratorlogin.php', '/administrator.php', '/administrators/', '/administrivia/', '/admin/leads.php', '/admin/list_gallery.php', 
    '/admin/login', '/adminLogin/', '/admin_login.asp', '/admin-login.asp', '/admin/login.asp', '/adminLogin.asp', '/admin/login-home.php', 
    '/admin_login.html', '/admin-login.html', '/admin/login.html', '/adminLogin.html', '/ADMIN/login.html', '/admin_login.php', 
    '/admin_login.php', '/admin-login.php', '/admin-login.php/', '/admin/login.php', '/adminLogin.php', '/ADMIN/login.php', 
    '/admin/login_success.php', '/admin/loginsuccess.php', '/admin/log.php', '/admin_main.html', '/admin/main_page.php', '/admin/main.php/', 
    '/admin/ManageAdmin.php', '/admin/manageImages.php', '/admin/manage_team.php', '/admin/member_home.php', '/admin/moderator.php', 
    '/admin/my_account.php', '/admin/myaccount.php', '/admin/overview.php', '/admin/page_management.php', '/admin/pages/home_admin.php', 
    '/adminpanel/', '/adminpanel.asp', '/adminpanel.html', '/adminpanel.php', '/admin.php', '/Admin/private/', '/adminpro/', 
    '/admin/product.php', '/admin/products.php', '/admins/', '/admins.asp', '/admin/save.php', '/admins.html', '/admin/slider.php', 
    '/admin/specializations.php', '/admins.php', '/admin_tool/', '/AdminTools/', '/admin/uhome.html', '/admin/upload.php', 
    '/admin/userpage.php', '/admin/viewblog.php', '/admin/viewmembers.php', '/admin/voucher.php', '/AdminWeb/', '/admin/welcomepage.php', 
    '/admin/welcome.php', '/admloginuser.asp', '/admloginuser.php', '/admon/', '/ADMON/', '/adm.php', '/affiliate.asp', '/affiliate.php', 
    '/auth/', '/auth/login/', '/authorize.php', '/autologin/', '/banneradmin/', '/base/admin/', '/bb-admin/', '/bbadmin/', 
    '/bb-admin/admin.asp', '/bb-admin/admin.html', '/bb-admin/admin.php', '/bb-admin/index.asp', '/bb-admin/index.html', '/bb-admin/index.php', 
    '/bb-admin/login.asp', '/bb-admin/login.html', '/bb-admin/login.php', '/bigadmin/', '/blogindex/', '/cadmins/', '/ccms/', 
    '/ccms/index.php', '/ccms/login.php', '/ccp14admin/', '/cms/', '/cms/admin/', '/cmsadmin/', '/cms/_admin/logon.php', '/cms/login/', 
    '/configuration/', '/configure/', '/controlpanel/', '/controlpanel.asp', '/controlpanel.html', '/controlpanel.php', '/cpanel/', 
    '/cPanel/', '/cpanel_file/', '/cp.asp', '/cp.html', '/cp.php', '/customer_login/', '/database_administration/', '/Database_Administration/', 
    '/db/admin.php', '/directadmin/', '/dir-login/', '/editor/', '/edit.php', '/evmsadmin/', '/ezsqliteadmin/', '/fileadmin/', 
    '/fileadmin.asp', '/fileadmin.html', '/fileadmin.php', '/formslogin/', '/forum/admin', '/globes_admin/', '/home.asp', '/home.html', 
    '/home.php', '/hpwebjetadmin/', '/include/admin.php', '/includes/login.php', '/Indy_admin/', '/instadmin/', '/interactive/admin.php', 
    '/irc-macadmin/', '/links/login.php', '/LiveUser_Admin/', '/login/', '/login1/', '/login.asp', '/login_db/', '/loginflat/', 
    '/login.html', '/login/login.php', '/login.php', '/login-redirect/', '/logins/', '/login-us/', '/logon/', '/logo_sysadmin/', 
    '/Lotus_Domino_Admin/', '/macadmin/', '/mag/admin/', '/maintenance/', '/manage_admin.php', '/manager/', '/manager/ispmgr/', 
    '/manuallogin/', '/memberadmin/', '/memberadmin.asp', '/memberadmin.php', '/members/', '/memlogin/', '/meta_login/', 
    '/modelsearch/admin.asp', '/modelsearch/admin.html', '/modelsearch/admin.php', '/modelsearch/index.asp', '/modelsearch/index.html', 
    '/modelsearch/index.php', '/modelsearch/login.asp', '/modelsearch/login.html', '/modelsearch/login.php', '/moderator/', 
    '/moderator/admin.asp', '/moderator/admin.html', '/moderator/admin.php', '/moderator.asp', '/moderator.html', '/moderator/login.asp', 
    '/moderator/login.html', '/moderator/login.php', '/moderator.php', '/moderator.php/', '/myadmin/', '/navSiteAdmin/', '/newsadmin/', 
    '/nsw/admin/login.php', '/openvpnadmin/', '/pages/admin/admin-login.asp', '/pages/admin/admin-login.html', '/pages/admin/admin-login.php', 
    '/panel/', '/panel-administracion/', '/panel-administracion/admin.asp', '/panel-administracion/admin.html', '/panel-administracion/admin.php', 
    '/panel-administracion/index.asp', '/panel-administracion/index.html', '/panel-administracion/index.php', '/panel-administracion/login.asp', 
    '/panel-administracion/login.html', '/panel-administracion/login.php', '/panelc/', '/paneldecontrol/', '/panel.php', '/pgadmin/', 
    '/phpldapadmin/', '/phpmyadmin/', '/phppgadmin/', '/phpSQLiteAdmin/', '/platz_login/', '/pma/', '/power_user/', '/project-admins/', 
    '/pureadmin/', '/radmind/', '/radmind-1/', '/rcjakar/admin/login.php', '/rcLogin/', '/server/', '/Server/', '/ServerAdministrator/', 
    '/server_admin_small/', '/Server.asp', '/Server.html', '/Server.php', '/showlogin/', '/simpleLogin/', '/site/admin/', '/siteadmin/', 
    '/siteadmin/index.asp', '/siteadmin/index.php', '/siteadmin/login.asp', '/siteadmin/login.html', '/site_admin/login.php', 
    '/siteadmin/login.php', '/smblogin/', '/sql-admin/', '/sshadmin/', '/ss_vms_admin_sm/', '/staradmin/', '/sub-login/', '/Super-Admin/', 
    '/support_login/', '/sys-admin/', '/sysadmin/', '/SysAdmin/', '/SysAdmin2/', '/sysadmin.asp', '/sysadmin.html', '/sysadmin.php', 
    '/sysadmins/', '/system_administration/', '/system-administration/', '/typo3/', '/ur-admin/', '/ur-admin.asp', '/ur-admin.html', 
    '/ur-admin.php', '/useradmin/', '/user.asp', '/user.html', '/UserLogin/', '/user.php', '/usuario/', '/usuarios/', '/usuarios//', 
    '/usuarios/login.php', '/utility_login/', '/vadmind/', '/vmailadmin/', '/webadmin/', '/WebAdmin/', '/webadmin/admin.asp', 
    '/webadmin/admin.html', '/webadmin/admin.php', '/webadmin.asp', '/webadmin.html', '/webadmin/index.asp', '/webadmin/index.html', 
    '/webadmin/index.php', '/webadmin/login.asp', '/webadmin/login.html', '/webadmin/login.php', '/webadmin.php', '/webmaster/', 
    '/websvn/', '/wizmysqladmin/', '/wp-admin/', '/wp-login/', '/wplogin/', '/wp-login.php', '/xlogin/', '/yonetici.asp', '/yonetici.html', 
    '/yonetici.php', '/yonetim.asp', '/yonetim.html', '/yonetim.php'
    
]

# Function to check if a URL is responsive
def check_admin_url(base_url, path):
    url = urljoin(base_url, path)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[+] Found Admin Login Page: {url}")
        else:
            print(f"[-] Not Found: {url} (Status Code: {response.status_code})")
    except requests.RequestException as e:
        print(f"[-] Error accessing {url}: {e}")

# Function to check all admin paths
def find_admin_pages(base_url):
    for path in admin_paths:
        check_admin_url(base_url, path)

# Main function to start the process
def start_checking(base_url):
    print(f"Starting Admin Page Search for {base_url}")
    find_admin_pages(base_url)

# User-friendly interface
def user_friendly_interface():
    website_url = input("Enter the website URL (e.g., https://example.com): ").strip()
    print(f"[*] Checking for admin login page at: {website_url}")
    start_checking(website_url)

if __name__ == "__main__":
    user_friendly_interface()
