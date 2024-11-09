import aiohttp
import asyncio
import random
import time
import logging
from tqdm import tqdm  # For progress bar
from colorama import Fore, Style
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Expanded admin paths list (sample paths provided; continue to 5k+ for production)
admin_paths = [
    # WordPress
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

    # Custom Applications & Web Apps
    '/admin', '/administrator', '/adminpanel', '/admin-dashboard', '/adminpage', '/admin-login-form', '/admin_login.php',
    '/user/admin', '/admin_dashboard', '/administrator-area', '/admin_backoffice', '/admin_console', '/admin/index.php',
    '/login/admin', '/admin-entry', '/admin_loginform', '/secureadmin', '/adminloginpath', '/admincheck', '/admin_loginpage',
    '/adminpage-check', '/admin/root', '/admincheckpath', '/admin_root-login', '/admin_entry/', '/admin-checkform', '/adminloginarea',
    '/admin_control', '/adminsettings', '/admin_admin', '/adminpanel123', '/admin_form', '/adminpanel_setup',
    '/admin-area.php', '/superadmin', '/admin/config', '/admin-settings', '/admin-set', '/admin-panel-root',

    # Admin Paths Used by Other CMS and Apps
    '/admin-console', '/adminpanel/check', '/admin-tools', '/adminsetup', '/adminctrl', '/admin-loginarea', '/admin_access.php',
    '/secureadmin-area', '/cpanel', '/backoffice', '/dashboard/login', '/admin-setup.php', '/controlpanel', '/admin-panal',

    # Generic Admin Paths (Common to many CMS and Apps)
    '/admin', '/administrator', '/admin-login', '/admin.php', '/adminlogin', '/administrator_login', '/admin-entrance',
    '/adminforms', '/adminloginform', '/admin-backoffice', '/secureadmin', '/admin-login-check', '/admin-loginroot',
    '/admin-loginindex', '/admin-console-form', '/admin_login-check', '/administrator-dashboard', '/admin-portal',
    '/admin-access', '/admin-checkform', '/user/admin', '/admin_login-page', '/admin-path-check', '/admin-root-path', '/admin-entry',
    
    # Additional Non-CMS Path Variations
    '/admin-tools', '/adminsetup', '/adminconfig', '/admin-auth', '/admin-controlpanel', '/admin_dashboard.php', '/user/adminpanel',
    '/admin-authentication', '/admin-config.php', '/administrator-area-check', '/adminroot-check', '/admin_forms.php',
    '/admin-control', '/admin_home', '/administrator-login-check', '/adminuserform', '/admin-enter', '/adminadminpage',
    '/admin-config-form', '/adminroot', '/adminpath', '/admin-config-check', '/admin-login-form.php', '/administrator-check',
    '/admin-panel-check', '/admin-page-setup', '/login/admin-check', '/admin-configuration', '/admin-controlpanel-login',
    '/admin-panel-login', '/admin_authentication', '/admin-logincheck', '/adminpaneladmin', '/admin-loginform-checker',
    '/admin_access-check', '/admin_checkpathform', '/admin_panel-setup', '/admin_panel_check', '/admin-entry-page', '/administrator-loginform',
    '/adminpanel-backend', '/adminuserform.php', '/admin_backoffice-form', '/administrator_loginform', '/adminbackoffice-check', '/admin-entry-check',
    '/admin_login_page-check', '/admin-configpath', '/admin-checkpath', '/admin-loging-page', '/admin-panel-checker',
    '/adminpage-access', '/admin-access-check', '/adminpath-checker', '/admin-check-access', '/adminuser-loginform', '/admin-entranceform'
]

    # Additional placeholder paths (continue to expand this list)
    '/admin', '/admin.php', '/adminpanel', '/administrator', '/admin123', '/admin/login', '/admin/login.php', '/administrator.php',
    '/admin_area', '/adminpanel/login', '/admin-login', '/adminpanel/index.php', '/admin_area.php', '/user/admin', '/wp-admin',
    '/admin-console', '/cpanel', '/admin-console/login', '/admin-control', '/admin_config', '/admin-dashboard', '/adminpanel-control',
    '/superadmin', '/adminarea', '/controlpanel', '/admin-login-page', '/admin-loginform', '/dashboard', '/adminpanel/admin',
    '/admin-dashboard.php', '/admin_auth', '/adminsetup', '/manager', '/admintools', '/admin-backoffice', '/admin-panel/login',
    '/adminform', '/secureadmin', '/admin_config.php', '/admin-area', '/admin_access', '/admin-user', '/admincheck', '/admin-portal',
    '/admin-setup.php', '/adminpage', '/admin_user_form', '/admin-backend', '/admin_controlpanel', '/administrator_login', '/admin_area-check',
    '/admin/dashboard', '/admin_path', '/admin-portal.php', '/adminzone', '/admin_login', '/admin-check', '/admin_page.php', '/admin12345',
    '/admin-config.php', '/admin_loginpage', '/adminpanel-check', '/admin_console.php', '/admin-dashboard-login', '/admin/dashboard.php',
    '/admin_login_area', '/adminpanel123', '/admin-login-form', '/admin-login-check', '/administratorarea', '/admin-entry', '/admin-login-area',
    '/admin-home', '/admin-entrance', '/admin_forms', '/login/admin', '/admin-loginindex', '/adminbackoffice', '/admincheck',
    '/admin-loginpath', '/user/adminpanel', '/securelogin', '/admin-password', '/admin_index.php', '/admin-control-form', '/admin-area-form',
    '/admin_login-check', '/admin_root', '/adminsetup.php', '/user/admin-login', '/admin-loginpage', '/administrator-login-form', '/admin_console-login',
    '/admin-panel-login', '/admin_area-login', '/administrator-login', '/admin-login-root', '/admin_userpage', '/admin-check-login',
    '/adminroot', '/admin-dashboard-form', '/admin-loginform.php', '/admin_login_area.php', '/admin_backoffice.php', '/admin_access.php',
    '/admin-logout', '/adminlogin.php', '/admin_console_login', '/adminpanel-setup', '/admin_config_area', '/admin-auth', '/admin_page-check',
    '/admin-check-path', '/adminlogin-path', '/admin-portal-form', '/admin_login-checker', '/adminpanel-dashboard', '/admin-login-area.php',
    '/adminbackoffice-form', '/admin-page-login', '/secureadmin-login', '/admin-access-form', '/admin-entry-form', '/administrator_index',
    '/admin_root-form', '/admin-login-checker.php', '/admin_controlpanel-login', '/admin-dashboard-check', '/admin-homepage', '/admin-loginpage.php',
    '/admin-tools-form', '/admin-loginform-check', '/admin_backend-login', '/adminpanel-login-page', '/admin-entry-check', '/admin_entrance.php',
    '/administrator-loginform', '/admin_page', '/adminpanel-login.php', '/admin-path-check', '/adminsetup-check', '/admin_index', '/admin-dashboard-check',
    '/admin-backend-check', '/adminpanel-form', '/admin-index-check', '/adminlogin-checker', '/admin-dashboard-access', '/admin-area-login-page',
    '/admin-root-login', '/administrator-access', '/admin-control-check', '/admincheckform', '/administrator-root-login', '/admin-checkpath.php',
    '/admin-panel-page', '/adminpage-check', '/admin-login-check', '/admin-backend-access', '/admin_root-check', '/admin_config_form',
    '/administrator_login.php', '/admin_check-login', '/admin-loginform-checker', '/admin-login-check-page', '/admin-backend-checker', '/admin_loginroot',
    '/adminpanel-login-check', '/admin-dashboard-area', '/admin-form', '/adminpanelform.php', '/admin_backoffice-login', '/admin_login',
    '/admin-backoffice-form.php', '/admin-login-rootform', '/admin-form-check', '/admin-dashboard-login.php', '/adminpanelroot', '/administrator-logincheck',
    '/admin-page-setup', '/admin-backoffice-check.php', '/adminroot-form', '/admin-logincheck', '/administrator_form', '/admin-entrance-form',
    '/admin_page-form', '/admin-dashboard-entry', '/administrator-root-check', '/admin_controlform', '/admin-authentication', '/admin-loginpath-form',
    '/admin_area_setup', '/admin-checkpathform', '/admin_config-form', '/administrator-loginpath', '/admin_loginpath-check',
    
    # Additional Paths
    '/admin', '/adminconsole', '/cpanel', '/backoffice', '/admin-dashboard', '/loginarea', '/controlpanel', '/adminforms',
    '/admincheck', '/adminconfig', '/superadmin', '/adminaccess', '/adminloginpage', '/adminpage', '/adminindex',
    '/admin-dashboard-check', '/admin-logincheck', '/adminpanel-root', '/adminpath', '/user/admin', '/adminpassword', '/adminuserform',
    '/adminlogin-check', '/administrator-login', '/admin-checkpathform', '/admin-login-root', '/admin-backendform', '/admin-area-check',
    '/admincheck-root', '/admin-login-checker', '/admin_loginpage', '/adminpanel-check', '/admin-authentication', '/adminloginindex',
    '/administratorform', '/admin-entrance', '/admin-backend-login', '/adminloginroot', '/adminpage-checker'
    
    
    # (Continue adding more paths to reach 5000 paths)
]

# List of User-Agent strings for rotation
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0 Safari/537.36'
]

# Random delay to prevent detection
def random_delay():
    time.sleep(random.uniform(0.5, 1.5))  # Reduced for speed

# Function to set headers with a randomized User-Agent
def get_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

# Check each admin page asynchronously
async def check_admin_page(session, url, path, semaphore):
    full_url = url + path
    headers = get_headers()
    try:
        async with semaphore, session.get(full_url, headers=headers, timeout=10) as response:
            status_code = response.status
            if status_code == 200:
                logger.info(f"{Fore.GREEN}[+] Found: {full_url}")
                return full_url
            elif status_code == 403:
                logger.info(f"{Fore.YELLOW}[!] Forbidden: {full_url} (403)")
            elif status_code == 404:
                return None
    except Exception as e:
        logger.error(f"{Fore.RED}Error checking {full_url}: {e}")
    finally:
        random_delay()
    return None

# Main async function to scan all paths
async def scan_admin_pages(url):
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(50)  # Controls concurrent requests
        tasks = [check_admin_page(session, url, path, semaphore) for path in admin_paths]
        results = []
        for future in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Scanning", unit=" paths"):
            result = await future
            if result:
                results.append(result)
        return results

# Run the program
def main():
    parser = argparse.ArgumentParser(description="Bukhari-Admin-Finder: Find Admin Login Pages")
    parser.add_argument("url", help="The base URL of the website (e.g., https://example.com)")
    args = parser.parse_args()

    print(f"{Fore.CYAN}Starting Bukhari-Admin-Finder...{Style.RESET_ALL}")
    url = args.url.rstrip('/')

    results = asyncio.run(scan_admin_pages(url))
    if results:
        print(f"\n{Fore.GREEN}Admin pages found:{Style.RESET_ALL}")
        for admin_url in results:
            print(f"{Fore.GREEN}{admin_url}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No admin pages found.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
