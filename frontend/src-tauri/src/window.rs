use tauri::{App, Manager};

pub fn configure_main_window(app: &App) -> Result<(), Box<dyn std::error::Error>> {
    let window = app.get_webview_window("main").expect("main window not found");

    // On macOS, set the window to floating panel level so it stays above other apps
    #[cfg(target_os = "macos")]
    {
        use tauri::Emitter;

        // Make the window visible
        window.show()?;

        // The window is already configured as always-on-top via tauri.conf.json
        // macOS private API gives us NSPanel-level floating behavior
        let _ = window.emit("window-ready", ());
    }

    #[cfg(target_os = "windows")]
    {
        use tauri::Emitter;
        window.show()?;
        let _ = window.emit("window-ready", ());
    }

    Ok(())
}
