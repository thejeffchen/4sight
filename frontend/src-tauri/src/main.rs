#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod window;

use std::process::{Child, Command};
use std::sync::Mutex;
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            window::configure_main_window(app)?;

            // Resolve the backend directory relative to the app
            let backend_dir = resolve_backend_dir();

            // Activate the venv and run uvicorn
            #[cfg(target_os = "macos")]
            let venv_python = backend_dir.join(".venv/bin/python");

            #[cfg(target_os = "windows")]
            let venv_python = backend_dir.join(".venv/Scripts/python.exe");
            let child = Command::new(&venv_python)
                .args(["-m", "uvicorn", "foresight.server:app", "--host", "127.0.0.1", "--port", "8742"])
                .current_dir(&backend_dir)
                .spawn()
                .expect("failed to start python backend — is the venv set up?");

            #[cfg(target_os = "windows")]
            {
                use std::os::windows::io::AsRawHandle;
                use windows_sys::Win32::System::JobObjects::*;

                unsafe {
                    let job = CreateJobObjectW(std::ptr::null(), std::ptr::null());
                    let mut info: JOBOBJECT_EXTENDED_LIMIT_INFORMATION = std::mem::zeroed();
                    info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
                    SetInformationJobObject(
                        job,
                        JobObjectExtendedLimitInformation,
                        &info as *const _ as *const std::ffi::c_void,
                        std::mem::size_of::<JOBOBJECT_EXTENDED_LIMIT_INFORMATION>() as u32,
                    );
                    AssignProcessToJobObject(job, child.as_raw_handle() as _);
                }
                // Job handle is leaked intentionally — it lives until the process exits,
                // at which point Windows closes it and kills all assigned processes.
            }

            app.manage(BackendProcess(Mutex::new(Some(child))));

            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while building tauri application")
        .run(|app, event| {
            if let tauri::RunEvent::Exit = event {
                if let Some(state) = app.try_state::<BackendProcess>() {
                    if let Ok(mut guard) = state.0.lock() {
                        if let Some(ref mut child) = *guard {
                            let _ = child.kill();
                            let _ = child.wait();
                        }
                    }
                }
            }
        });
}

struct BackendProcess(Mutex<Option<Child>>);

fn resolve_backend_dir() -> std::path::PathBuf {
    // In development, the backend is at ../../backend relative to src-tauri
    let dev_path = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../backend");
    if dev_path.exists() {
        return dev_path.canonicalize().unwrap();
    }

    // Fallback: look relative to the executable
    let exe_dir = std::env::current_exe()
        .expect("cannot find executable path")
        .parent()
        .unwrap()
        .to_path_buf();
    #[cfg(target_os = "macos")]
    { exe_dir.join("../Resources/backend") }

    #[cfg(target_os = "windows")]
    { exe_dir.join("../backend") }
}
