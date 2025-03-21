/**
 * Main JavaScript file for the Hệ thống báo cáo
 */

document.addEventListener('DOMContentLoaded', function() {
    // Enable multi-level dropdowns on hover for desktop
    setupMultiLevelMenu();
    
    // Add active class to current menu item
    highlightCurrentPage();
});

/**
 * Thiết lập menu đa cấp
 */
function setupMultiLevelMenu() {
    // Only use hover for desktop devices
    if (window.innerWidth >= 992) {
        document.querySelectorAll('.dropdown-menu .dropdown-toggle').forEach(function(element) {
            element.addEventListener('mouseover', function() {
                let nextEl = this.nextElementSibling;
                if (nextEl && nextEl.classList.contains('dropdown-menu')) {
                    // Adjust position if menu would go off-screen
                    let parent = this.offsetParent;
                    let offset = parent.offsetLeft + parent.offsetWidth;
                    let screenWidth = window.innerWidth;
                    let menuWidth = nextEl.offsetWidth;
                    
                    if (offset + menuWidth > screenWidth) {
                        nextEl.classList.add('dropdown-submenu-left');
                    } else {
                        nextEl.classList.remove('dropdown-submenu-left');
                    }
                    
                    // Show the menu
                    nextEl.style.display = 'block';
                }
            });
            
            // Hide on mouseout
            element.addEventListener('mouseout', function() {
                let nextEl = this.nextElementSibling;
                if (nextEl && nextEl.classList.contains('dropdown-menu')) {
                    nextEl.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Đánh dấu menu hiện tại
 */
function highlightCurrentPage() {
    const currentUrl = window.location.pathname;
    
    // Find all links in the navigation
    document.querySelectorAll('.navbar-nav a').forEach(function(link) {
        // Remove any existing active class
        link.classList.remove('active');
        
        // If the link href matches the current URL
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
            
            // Highlight parent dropdown items
            let parent = link.parentElement;
            while (parent) {
                if (parent.classList.contains('dropdown-menu')) {
                    let parentToggle = parent.previousElementSibling;
                    if (parentToggle && parentToggle.classList.contains('dropdown-toggle')) {
                        parentToggle.classList.add('active');
                    }
                }
                parent = parent.parentElement;
            }
        }
    });
}

/**
 * Hàm để định dạng số tiền
 * @param {number} amount - Số tiền cần định dạng
 * @param {string} currency - Đơn vị tiền tệ (mặc định: VNĐ)
 * @returns {string} Chuỗi đã được định dạng
 */
function formatCurrency(amount, currency = 'VNĐ') {
    return amount.toLocaleString('vi-VN') + ' ' + currency;
}

/**
 * Hàm để xuất dữ liệu sang Excel
 * @param {HTMLTableElement} table - Bảng cần xuất
 * @param {string} filename - Tên file xuất ra
 */
function exportTableToExcel(table, filename = 'export') {
    // Chức năng này sẽ được phát triển sau
    console.log('Export to Excel: ', table, filename);
}

/**
 * Hàm để xuất dữ liệu sang PDF
 * @param {HTMLTableElement} table - Bảng cần xuất
 * @param {string} filename - Tên file xuất ra
 */
function exportTableToPDF(table, filename = 'export') {
    // Chức năng này sẽ được phát triển sau
    console.log('Export to PDF: ', table, filename);
}