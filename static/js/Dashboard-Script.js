// Initialize active tab based on user role
window.onload = function () {
    const userRole = document.body.dataset.userRole;

    // Map roles to default tabs
    const roleToTab = {
        admin: 'admin-home',
        instructor: 'instructor-home',
        student: 'student-home'
    };

    // Determine the default tab for the current role
    const defaultTab = roleToTab[userRole];
    if (defaultTab) {
        showTab(defaultTab);
    }

    // Add active class to the default tab link
    const defaultLink = document.querySelector(`[onclick="showTab('${defaultTab}')"]`);
    if (defaultLink) {
        defaultLink.classList.add('active');
    }
};

// Function to hide all tabs
function hideAllTabs() {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.classList.add('hidden');
        tab.classList.remove('active');
    });
}

// Function to show a specific tab
function showTab(tabName) {
    hideAllTabs(); // Hide all tabs first

    // Show the selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
        selectedTab.classList.remove('hidden');
    } else {
        console.error(`Tab "${tabName}" not found.`);
    }

    // Update active state of navigation links
    const links = document.querySelectorAll('.tab-link');
    links.forEach(link => {
        link.classList.remove('active');
    });

    // Add active class to clicked link
    const selectedLink = document.querySelector(`[onclick="showTab('${tabName}')"]`);
    if (selectedLink) {
        selectedLink.classList.add('active');
    }
}
