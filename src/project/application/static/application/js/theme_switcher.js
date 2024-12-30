// Enum for theme options
const THEMES = {
    DARK: 'dark',
    LIGHT: 'light',
    SYSTEM: 'system',
}

$(document).ready(function () {
    // The hidden select box to choose themes from.
    const theme_select_box = $("#theme");
    // Icon for light mode.
    const light_mode_icon = $("#light-mode");
    // Icon for dark mode.
    const dark_mode_icon = $("#dark-mode");
    // Icon for following the system's theme.
    const system_mode_icon = $("#follow-system");

    /*
    * Swaps the current theme to the next theme, and displays the correct icon.
    * current_icon: The current icon being displayed to the user.
    * next_theme: The theme to switch to next.
    * next_icon: The icon representing the next theme to be displayed.
     */
    function _swapTheme(current_icon, next_theme, next_icon){
        current_icon.hide();
        next_icon.fadeIn();
        theme_select_box.val(next_theme);
        document.cookie = `theme_preference=${next_theme}`;
    }

    /*
    * The flow for switching themes(system -> dark -> light).
     */
    function updateTheme() {
        let current_theme = theme_select_box.val();
        if(current_theme === "system")
            _swapTheme(system_mode_icon,THEMES.DARK, dark_mode_icon);
        else if(current_theme === "dark")
            _swapTheme(dark_mode_icon,THEMES.LIGHT, light_mode_icon);
        else if(current_theme === "light")
            _swapTheme(light_mode_icon,THEMES.SYSTEM, system_mode_icon);
        else
            console.error(`Unknown theme: ${current_theme}`);
    }

    // Set up the event listeners on the icons.
    light_mode_icon.click(updateTheme);
    dark_mode_icon.click(updateTheme);
    system_mode_icon.click(updateTheme);

    const cookies = decodeURIComponent(document.cookie).split(";");
    for(let cookie of cookies){
        cookie = cookie.toLowerCase().trim();
        if(cookie === `theme_preference=${THEMES.DARK}`)
            system_mode_icon.click();
        if(cookie === `theme_preference=${THEMES.LIGHT}`) {
            system_mode_icon.click();
            dark_mode_icon.click();
        }
    }

});