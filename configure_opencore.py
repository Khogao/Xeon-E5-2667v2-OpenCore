"""
configure_opencore.py — Xeon E5-2667v2 + Huananzhi X79 + RX 580 OpenCore Config
===================================================================================
Script tự động cấu hình config.plist từ Sample.plist hoặc config.plist hiện có.

Phần cứng đã xác nhận (WMI scan):
  - CPU    : Intel Xeon E5-2667 v2 (Ivy Bridge-EP, 8C/16T) — LGA2011 X79
  - Board  : HUANANZHI X79 V2.49PB (C200/C600 chipset, AMI BIOS 4.6.5)
  - GPU    : AMD RX 580 Polaris (VEN_1002 DEV_67DF) — native macOS
  - Audio  : Realtek ALC887 (HDAUDIO VEN_10EC DEV_0887) — layout-id 1
  - ETH    : Realtek RTL8168 (PCI VEN_10EC DEV_8168) — RealtekRTL8111.kext
  - WiFi   : Broadcom BCM43602 (VEN_14E4 DEV_43BA SUBSYS_0133106B) — native
  - BT     : Apple Broadcom (USB VID_05AC PID_8290) — native
  - USB2   : Intel C200 EHCI DEV_1C26 + DEV_1C2D
  - USB3   : VIA VL805 (VEN_1106 DEV_3483)

Target: macOS Sequoia 15.x, OpenCore 1.0.6, SMBIOS MacPro6,1

CÁCH DÙNG:
  1. Copy Sample.plist từ OpenCore Docs vào EFI/OC/ và đổi tên thành config.plist
  2. Chạy: python configure_opencore.py
  3. Điền SMBIOS (serial, MLB, UUID) bằng GenSMBIOS TRƯỚC khi cài
  4. Copy kexts vào EFI/OC/Kexts/, ACPI vào EFI/OC/ACPI/
"""

import plistlib
import os
import sys
import uuid
import shutil

# ─── PATHS ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OC_ROOT    = os.path.join(SCRIPT_DIR, "EFI", "OC")
CONFIG_PATH = os.path.join(OC_ROOT, "config.plist")
SAMPLE_PATH = os.path.normpath(os.path.join(
    SCRIPT_DIR, "Updates", "OpenCore_Extracted", "Docs", "Sample.plist"
))

# ─── KEXT LOAD ORDER ─────────────────────────────────────────────────────────
KEXT_ORDER = {
    "Lilu.kext":             0,   # luôn đầu tiên
    "VirtualSMC.kext":       1,   # trước SMC plugins
    "SMCProcessor.kext":     2,
    "SMCSuperIO.kext":       2,
    "WhateverGreen.kext":    3,
    "AppleALC.kext":         4,
    "CpuTscSync.kext":       5,   # BẮT BUỘC X79 — đồng bộ TSC
    "RealtekRTL8111.kext":   6,
    "USBToolBox.kext":       7,   # USB kext driver
    "UTBMap.kext":           8,   # USB map — sau driver
}

def kext_priority(name):
    return KEXT_ORDER.get(name, 99)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def ensure_key(d, key, default):
    if key not in d:
        d[key] = default
    return d[key]

def walk_kexts(kext_dir):
    """Trả về list kext entries cho Kernel -> Add, kể cả PlugIns."""
    entries = []
    if not os.path.isdir(kext_dir):
        print(f"  [!] Kexts dir không tồn tại: {kext_dir}")
        return entries

    top_kexts = sorted(
        [f for f in os.listdir(kext_dir) if f.endswith(".kext")],
        key=kext_priority
    )

    for kext in top_kexts:
        kext_path = os.path.join(kext_dir, kext)
        executable = find_executable(kext_path, kext)
        entries.append(make_kext_entry(kext, executable))

        # Scan PlugIns
        plugins_dir = os.path.join(kext_path, "Contents", "PlugIns")
        if os.path.isdir(plugins_dir):
            for plugin in sorted(os.listdir(plugins_dir)):
                if plugin.endswith(".kext"):
                    plugin_path = os.path.join(plugins_dir, plugin)
                    plugin_exe  = find_executable(plugin_path, plugin)
                    entries.append(make_kext_entry(
                        f"{kext}/Contents/PlugIns/{plugin}", plugin_exe
                    ))
    return entries

def find_executable(kext_path, kext_name):
    """Tìm executable thực sự bên trong kext."""
    macos_dir = os.path.join(kext_path, "Contents", "MacOS")
    if os.path.isdir(macos_dir):
        files = os.listdir(macos_dir)
        if files:
            return f"Contents/MacOS/{files[0]}"
    return ""

def make_kext_entry(bundle_path, executable_path, enabled=True):
    return {
        "Arch":           "x86_64",
        "BundlePath":     bundle_path,
        "Comment":        "",
        "Enabled":        enabled,
        "ExecutablePath": executable_path,
        "MaxKernel":      "",
        "MinKernel":      "",
        "PlistPath":      "Contents/Info.plist",
    }

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    # Kiểm tra config.plist hoặc Sample.plist
    if not os.path.exists(CONFIG_PATH):
        if os.path.exists(SAMPLE_PATH):
            print(f"config.plist không có — copy từ Sample.plist...")
            os.makedirs(OC_ROOT, exist_ok=True)
            shutil.copy(SAMPLE_PATH, CONFIG_PATH)
        else:
            print("LỖI: Không tìm thấy config.plist hoặc Sample.plist.")
            print(f"  Tìm ở: {CONFIG_PATH}")
            print(f"  Tìm ở: {SAMPLE_PATH}")
            sys.exit(1)

    print(f"Đang load: {CONFIG_PATH}")
    with open(CONFIG_PATH, "rb") as f:
        config = plistlib.load(f)

    # ── 1. ACPI ──────────────────────────────────────────────────────────────
    print("[1] Cập nhật ACPI...")
    acpi_dir = os.path.join(OC_ROOT, "ACPI")
    acpi_files = []
    if os.path.isdir(acpi_dir):
        acpi_files = [f for f in os.listdir(acpi_dir) if f.endswith(".aml")]

    config["ACPI"]["Add"] = [
        {"Comment": f, "Enabled": True, "Path": f} for f in acpi_files
    ]
    # Xeon Ivy Bridge-EP KHÔNG cần Drop CpuPm/Cpu0Ist (chỉ Sandy Bridge)
    config["ACPI"]["Delete"] = []
    config["ACPI"]["Patch"]  = []

    # ── 2. Booter ────────────────────────────────────────────────────────────
    print("[2] Cấu hình Booter quirks...")
    q = config["Booter"]["Quirks"]
    q["AvoidRuntimeDefrag"]        = True
    q["DevirtualiseMmio"]          = True
    q["SetupVirtualMap"]           = True
    q["SyncRuntimePermissions"]    = True
    q["ProtectUefiServices"]       = False
    q["EnableSafeModeSlide"]       = True
    q["ProvideCustomSlide"]        = True  # giữ tính năng KASLR

    # ── 3. DeviceProperties ──────────────────────────────────────────────────
    print("[3] DeviceProperties...")
    dp = ensure_key(config["DeviceProperties"], "Add", {})

    # Audio: Realtek ALC887 — path cần verify bằng Hackintool sau cài
    # Thường trên X79 là PciRoot(0x0)/Pci(0x1b,0x0)
    audio_path = "PciRoot(0x0)/Pci(0x1b,0x0)"
    ensure_key(dp, audio_path, {})
    dp[audio_path]["layout-id"] = b'\x01\x00\x00\x00'  # layout-id = 1

    # GPU RX 580 — native, KHÔNG inject frame buffer
    # KHÔNG thêm DeviceProperties cho GPU (không cần)

    # Ethernet Realtek RTL8168 — built-in flag
    # Path cần verify bằng Hackintool; thường là PciRoot(0x0)/Pci(0x1c,0x0)/Pci(0x0,0x0) trên X79
    # eth_path = "PciRoot(0x0)/Pci(0x1c,0x0)/Pci(0x0,0x0)"
    # ensure_key(dp, eth_path, {})
    # dp[eth_path]["built-in"] = b'\x01'

    # ── 4. Drivers ───────────────────────────────────────────────────────────
    print("[4] Cập nhật Drivers...")
    drivers_dir = os.path.join(OC_ROOT, "Drivers")
    driver_files = []
    if os.path.isdir(drivers_dir):
        driver_files = [f for f in os.listdir(drivers_dir) if f.endswith(".efi")]

    drivers_config = []
    # OpenRuntime — bắt buộc, load sớm
    if "OpenRuntime.efi" in driver_files:
        drivers_config.append({
            "Arguments": "", "Comment": "Required", "Enabled": True,
            "LoadEarly": True, "Path": "OpenRuntime.efi"
        })
        driver_files.remove("OpenRuntime.efi")

    # KHÔNG dùng OpenVariableRuntimeDxe — BIOS desktop có native NVRAM

    for f in sorted(driver_files):
        drivers_config.append({
            "Arguments": "", "Comment": "", "Enabled": True,
            "LoadEarly": False, "Path": f
        })
    config["UEFI"]["Drivers"] = drivers_config

    # ── 5. Kernel ────────────────────────────────────────────────────────────
    print("[5] Cập nhật Kexts...")
    kext_dir = os.path.join(OC_ROOT, "Kexts")
    config["Kernel"]["Add"] = walk_kexts(kext_dir)
    print(f"  Tìm thấy {len(config['Kernel']['Add'])} kext entries")

    # Kernel Quirks
    q = config["Kernel"]["Quirks"]
    q["AppleCpuPmCfgLock"]        = True   # BIOS Huananzhi X79 không unlock CFG Lock
    q["AppleXcpmCfgLock"]         = True   # Cần cho Ivy Bridge-EP
    q["DisableIoMapper"]          = True   # Disable VT-d mapping
    q["DisableLinkeditJettison"]  = True   # Ổn định kext loading
    q["LapicKernelPanic"]         = False  # Không cần trên desktop
    q["PanicNoKextDump"]          = True   # Debug dễ hơn
    q["PowerTimeoutKernelPanic"]  = True   # Tránh panic vì timeout
    q["XhciPortLimit"]            = False  # Dùng USBToolBox map từ Windows

    # Clear entries mẫu — Ivy Bridge-EP không cần chúng
    config["Kernel"]["Block"]  = []
    config["Kernel"]["Patch"]  = []
    config["Kernel"]["Force"]  = []

    # ── 6. Misc ──────────────────────────────────────────────────────────────
    print("[6] Misc...")
    config["Misc"]["Boot"]["LauncherOption"]   = "Full"
    config["Misc"]["Boot"]["PickerMode"]        = "External"
    config["Misc"]["Boot"]["PickerVariant"]     = "Acidanthera\\GoldenGate"
    config["Misc"]["Boot"]["PollAppleHotKeys"]  = True
    config["Misc"]["Boot"]["HideAuxiliary"]     = True
    config["Misc"]["Boot"]["Timeout"]           = 5

    config["Misc"]["Debug"]["AppleDebug"]      = True
    config["Misc"]["Debug"]["ApplePanic"]      = True
    config["Misc"]["Debug"]["DisableWatchDog"] = True   # Tránh timeout khi boot chậm
    config["Misc"]["Debug"]["Target"]          = 67    # file + serial logging

    config["Misc"]["Security"]["AllowSetDefault"]    = True
    config["Misc"]["Security"]["DmgLoading"]         = "Any"       # Recovery image không signed
    config["Misc"]["Security"]["ScanPolicy"]         = 0
    config["Misc"]["Security"]["SecureBootModel"]    = "Disabled"  # Cần cho Ivy Bridge + OCLP
    config["Misc"]["Security"]["Vault"]              = "Optional"

    # Tools
    tools_dir = os.path.join(OC_ROOT, "Tools")
    if os.path.isdir(tools_dir):
        tool_files = [f for f in os.listdir(tools_dir) if f.endswith(".efi")]
        config["Misc"]["Tools"] = [{
            "Arguments": "", "Auxiliary": True, "Comment": f,
            "Enabled": True, "Flavour": "Auto", "FullNvramAccess": False,
            "Name": f.replace(".efi", ""), "Path": f,
            "RealPath": False, "TextMode": False
        } for f in sorted(tool_files)]

    # ── 7. NVRAM ─────────────────────────────────────────────────────────────
    print("[7] NVRAM...")
    key_7c = "7C436110-AB2A-4BBB-A880-FE41995C9F82"
    ensure_key(config["NVRAM"]["Add"], key_7c, {})
    nv = config["NVRAM"]["Add"][key_7c]

    # Boot-args — npci=0x3000 BẮT BUỘC trên X79
    nv["boot-args"]        = "-v keepsyms=1 debug=0x100 npci=0x3000 alcid=1"
    nv["csr-active-config"] = b'\x03\x00\x00\x00'  # SIP partially disabled cho OCLP
    nv["prev-lang:kbd"]    = "en-US:0"

    # KHÔNG dùng NVRAM emulation — native BIOS
    config["NVRAM"]["LegacyEnable"]    = False
    config["NVRAM"]["LegacyOverwrite"] = False
    config["NVRAM"]["WriteFlash"]      = True

    # ── 8. PlatformInfo ──────────────────────────────────────────────────────
    print("[8] PlatformInfo — MacPro6,1...")
    gen = config["PlatformInfo"]["Generic"]
    gen["SystemProductName"] = "MacPro6,1"
    gen["ROM"]               = bytes.fromhex("F45C89A5508F")  # WiFi MAC address

    # SMBIOS — PHẢI generate bằng GenSMBIOS, KHÔNG dùng giá trị mẫu này!
    # https://github.com/corpnewt/GenSMBIOS
    # Chạy: python3 GenSMBIOS.py → 3. Generate SMBIOS → MacPro6,1
    PLACEHOLDER_SERIAL = "CHANGEME_RUN_GENSMBIOS"
    PLACEHOLDER_MLB    = "CHANGEME_RUN_GENSMBIOS"
    if gen.get("SystemSerialNumber", "").startswith("CHANGEME") or gen.get("SystemSerialNumber", "") == "":
        gen["SystemSerialNumber"] = PLACEHOLDER_SERIAL
        gen["MLB"]                = PLACEHOLDER_MLB
        gen["SystemUUID"]         = str(uuid.uuid4()).upper()
        print("  ⚠️  SMBIOS chứa PLACEHOLDER — chạy GenSMBIOS trước khi dùng!")
    else:
        print(f"  Serial hiện tại: {gen['SystemSerialNumber'][:8]}... (đã có)")

    config["PlatformInfo"]["UpdateDataHub"]    = True
    config["PlatformInfo"]["UpdateNVRAM"]      = True
    config["PlatformInfo"]["UpdateSMBIOS"]     = True
    config["PlatformInfo"]["UpdateSMBIOSMode"] = "Create"

    # ── 9. UEFI ──────────────────────────────────────────────────────────────
    print("[9] UEFI quirks...")
    uq = config["UEFI"]["Quirks"]
    uq["IgnoreInvalidFlexRatio"] = True   # BẮT BUỘC Sandy Bridge VÀ Ivy Bridge-E — Dortania guide
    uq["ReleaseUsbOwnership"]    = True   # Nhường USB từ BIOS cho OS
    uq["RequestBootVarRouting"]  = True   # Cần cho LauncherOption=Full
    uq["UnblockFsConnect"]       = False  # Không phải HP
    uq["ResizeGpuBars"]          = -1     # Không dùng Resizable BAR

    config["UEFI"]["APFS"]["MinDate"]    = -1  # Cho phép mọi phiên bản APFS
    config["UEFI"]["APFS"]["MinVersion"] = -1

    # ── Lưu ──────────────────────────────────────────────────────────────────
    print(f"\nLưu config.plist → {CONFIG_PATH}")
    with open(CONFIG_PATH, "wb") as f:
        plistlib.dump(config, f)

    # ── Tóm tắt ──────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("✅  configure_opencore.py hoàn thành!")
    print("="*60)
    print("""
CHECKLIST TRƯỚC KHI BOOT:
  [ ] Chạy GenSMBIOS → thay CHANGEME_RUN_GENSMBIOS bằng serial MacPro6,1 thực
  [ ] Copy kexts vào EFI/OC/Kexts/:
        Lilu, VirtualSMC, SMCProcessor, SMCSuperIO
        WhateverGreen, AppleALC, CpuTscSync (BẮT BUỘC X79!)
        RealtekRTL8111, USBToolBox, UTBMap (từ USBToolBox Windows.exe)
  [ ] Copy SSDT/ACPI vào EFI/OC/ACPI/:
        SSDT-EC.aml, SSDT-PLUG.aml, SSDT-USBX.aml
        SSDT-PM.aml (tạo sau boot bằng ssdtPRGen.sh)
  [ ] BIOS: BẬT "Above 4G Decoding" — BẮT BUỘC (Dortania Ivy Bridge-E HEDT)
  [ ] BIOS: 'AppleCpuPmCfgLock' + 'AppleXcpmCfgLock' = YES (đã set)
  [ ] boot-args bao gồm 'npci=0x3000' (đã set)
  [ ] Sau cài: chạy OCLP → Post-Install Root Patch cho Ivy Bridge
""")


if __name__ == "__main__":
    main()
