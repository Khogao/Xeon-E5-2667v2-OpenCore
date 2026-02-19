# Hackintosh Desktop: Xeon E5-2667 v2 + RX 580 (Huananzhi X79)

> **Ngôn ngữ**: Tiếng Việt | **Cập nhật lần cuối**: Tháng 2/2026
> **Target OS**: macOS Sequoia 15.x | **Bootloader**: OpenCore 1.0.6 | **OCLP**: 2.4.1
> **Trạng thái**: Đang setup  chưa cài xong

---

## Mục lục

1. [Cấu hình máy](#1-cấu-hình-máy)
2. [Giai đoạn 1  Tải file cần thiết](#2-giai-đoạn-1--tải-file-cần-thiết)
3. [Giai đoạn 2  Chỉnh BIOS](#3-giai-đoạn-2--chỉnh-bios)
4. [Giai đoạn 3  Map USB từ Windows](#4-giai-đoạn-3--map-usb-từ-windows)
5. [Giai đoạn 4  Tạo USB cài đặt](#5-giai-đoạn-4--tạo-usb-cài-đặt)
6. [Giai đoạn 5  Edit config.plist](#6-giai-đoạn-5--edit-configplist)
7. [Giai đoạn 6  Cài macOS](#7-giai-đoạn-6--cài-macos)
8. [Giai đoạn 7  Post-Install](#8-giai-đoạn-7--post-install)
9. [Troubleshooting](#9-troubleshooting)
10. [Tham khảo & Nguồn](#10-tham-khảo--nguồn)

---

## 1. Cấu hình máy

> Đã xác nhận qua WMI scan trực tiếp trên Windows.

| Thành phần | Chi tiết | Ghi chú |
|---|---|---|
| **CPU** | Intel Xeon E5-2667 v2 @ 3.30GHz  Ivy Bridge-EP, 8C/16T, L3 25MB | LGA2011, socket X79 |
| **Mainboard** | **HUANANZHI X79 V2.49PB**  C200/C600 Chipset, Intel Q65 LPC (`DEV_1C4C`) | AMI BIOS 4.6.5 |
| **GPU** | AMD Radeon RX 580 Series  Polaris 10, 4GB, `DEV_67DF` | Native macOS High Sierra  Sequoia |
| **RAM** | 48 GB Samsung DDR3 ECC 1333MHz  4 DIMM (16GB2 + 8GB2) | Samsung M393 series |
| **WiFi** | **Broadcom BCM43602** Apple OEM  `VEN_14E4 DEV_43BA SUBSYS_0133106B` | Native macOS, KHÔNG cần kext |
| **Bluetooth** | Apple Broadcom Built-in  `USB\VID_05AC PID_8290` | Native macOS, KHÔNG cần kext |
| **Ethernet** | **Realtek RTL8168/8111**  `PCI\VEN_10EC DEV_8168` | Cần `RealtekRTL8111.kext` |
| **Audio** | **Realtek ALC887**  `HDAUDIO\VEN_10EC DEV_0887` | AppleALC layout-id: **1** |
| **USB 2.0** | Intel C200 EHCI  `DEV_1C26` + `DEV_1C2D` | 2 controller |
| **USB 3.0** | **VIA VL805**  `VEN_1106 DEV_3483` | PCIe add-in card |
| **ổ cứng macOS** | Apple SSD SM0128G 128GB + Samsung 850 EVO 120GB | APFS RAID 0 ~240GB |
| **ổ cứng Windows** | SK Hynix HFS256G32MND 256GB | Boot Windows |
| **ổ cứng data** | Seagate 1TB HDD | Time Machine / Dữ liệu |

### SMBIOS & Platform

| | |
|---|---|
| **SMBIOS** | `MacPro6,1`  Mac Pro Late 2013, Ivy Bridge-EP Xeon |
| **Board ID (Sequoia)** | `Mac-937A206F2EE63C01` |
| **OpenCore** | 1.0.6 |
| **OCLP** | 2.4.1 |

> `MacPro6,1` là lựa chọn đúng duy nhất cho Xeon E5 v2  cùng kiến trúc Ivy Bridge-EP.
> Confirmed bởi: [mokk731/X79-E5v2-OpenCore-EFI](https://github.com/mokk731/X79-E5v2-OpenCore-EFI), [nguyenphucdev/OpenCore_X79_X99_Xeon](https://github.com/nguyenphucdev/OpenCore_X79_X99_Xeon_E5_2650v2).

### Kế hoạch ổ cứng: APFS RAID 0

> Gộp **Apple SSD 128GB + Samsung 850 EVO 120GB** = **~240GB** cho macOS.
> 128GB đơn lẻ không đủ khi cài nhiều app/tool. APFS RAID 0 native trên macOS 10.14+.

| Phương án | Dung lượng | Tốc độ | Ghi chú |
|---|---|---|---|
| **APFS RAID 0** (ưu tiên) | ~240 GB | ~2x sequential | 1 ổ chết = mất hết  backup bắt buộc |
| Chỉ Apple SSD | 128 GB | Bình thường | Dự phòng nếu RAID lỗi |

---

## 2. Giai đoạn 1  Tải file cần thiết

> Toàn bộ chạy từ **Windows** trước khi đụng đến macOS.

### 2.1 OpenCore

Tải **OpenCorePkg 1.0.6** bản `RELEASE`:
 [github.com/acidanthera/OpenCorePkg/releases](https://github.com/acidanthera/OpenCorePkg/releases)

Giải nén, lấy từ `X64/EFI/`:
- `OC/OpenCore.efi`
- `BOOT/BOOTx64.efi`
- Drivers: `OpenRuntime.efi`, `OpenCanopy.efi`, `HfsPlusLegacy.efi`

### 2.2 Kexts

Tải tất cả bản `RELEASE` mới nhất:

| Kext | Link | Phiên bản | Ghi chú |
|---|---|---|---|
| **Lilu** | [acidanthera/Lilu](https://github.com/acidanthera/Lilu/releases) | 1.7.1 | Nạp đầu tiên |
| **VirtualSMC** | [acidanthera/VirtualSMC](https://github.com/acidanthera/VirtualSMC/releases) | 1.3.7 | Kèm SMCProcessor + SMCSuperIO |
| **WhateverGreen** | [acidanthera/WhateverGreen](https://github.com/acidanthera/WhateverGreen/releases) | 1.7.0 | GPU + DRM |
| **AppleALC** | [acidanthera/AppleALC](https://github.com/acidanthera/AppleALC/releases) | 1.9.6 | Audio ALC887 |
| **CpuTscSync** | [acidanthera/CpuTscSync](https://github.com/acidanthera/CpuTscSync/releases) | 1.1.2 | BẮT BUỘC X79  thiếu = treo chắc chắn |
| **RealtekRTL8111** | [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X/releases) | v3.0.0 | Ethernet RTL8168 |
| **USBToolBox** | [USBToolBox/kext](https://github.com/USBToolBox/kext/releases) | 1.2.0 | USB kext (dùng với UTBMap) |

> Không cần WiFi/BT kext  BCM43602 (`SUBSYS_0133106B` = Apple OEM) và BT (`VID_05AC`) native.
> Không cần IntelMausi  máy dùng Realtek RTL8168, không phải Intel NIC.
> Confirmed: [antipeth/EFI-Motherboard-X79-OpenCore-Hackintosh](https://github.com/antipeth/EFI-Motherboard-X79-OpenCore-Hackintosh)  cùng Huananzhi X79.

### 2.3 Tools

| Tool | Link | Mục đích |
|---|---|---|
| **USBToolBox.exe** | [USBToolBox/tool/releases](https://github.com/USBToolBox/tool/releases) | Map USB từ Windows |
| **GenSMBIOS** | [corpnewt/GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) | Generate serial MacPro6,1 |
| **ProperTree** | [corpnewt/ProperTree](https://github.com/corpnewt/ProperTree) | Edit config.plist |
| **MountEFI** | [corpnewt/MountEFI](https://github.com/corpnewt/MountEFI) | Mount EFI partition sau cài |
| **Hackintool** | [benbaker76/Hackintool](https://github.com/benbaker76/Hackintool/releases) | Verify PCIe path, USB, audio (sau cài) |
| **OCLP 2.4.1** | [dortania/OpenCore-Legacy-Patcher](https://github.com/dortania/OpenCore-Legacy-Patcher/releases) | Root patch Ivy Bridge sau cài |

### 2.4 macOS Sequoia Recovery

Đã tải  `BaseSystem.dmg` (843.4MB) tại `_tmp/sequoia_recovery/com.apple.recovery.boot/`

```powershell
# Nếu cần tải lại (board ID chính xác cho Sequoia 15):
$python = "C:\Users\Phi\AppData\Local\Programs\Python\Python311\python.exe"
$macrecovery = ".\Updates\OpenCore_Extracted\Utilities\macrecovery\macrecovery.py"
& $python $macrecovery -b Mac-937A206F2EE63C01 -m 00000000000000000 download
```

> Board ID `Mac-937A206F2EE63C01` = MacPro7,1  dùng để tải Sequoia 15.
> Ivy Bridge + Sequoia 15.7.x confirmed hoạt động  Reddit r/hackintosh 2026, OCLP 2.4.1 release notes.

### 2.5 ACPI SSDTs

Tải prebuilt từ [dortania/Getting-Started-With-ACPI](https://github.com/dortania/Getting-Started-With-ACPI):

| File | Ghi chú |
|---|---|
| `SSDT-EC.aml` | Dummy EC, cần Catalina+ |
| `SSDT-PLUG.aml` | XCPM plugin type, Ivy Bridge |
| `SSDT-USBX.aml` | USB power injection |
| `SSDT-PM.aml` | Tạo sau cài bằng `ssdtPRGen.sh`  làm ở Giai đoạn 7 |

> `SSDT-IMEI.aml` không cần  chipset X79 C600/C200 native.
> `SSDT-RTC0-RANGE.aml`  thêm nếu gặp lỗi RTC khi boot.

---

## 3. Giai đoạn 2  Chỉnh BIOS

> BIOS: Huananzhi X79 V2.49PB  AMI BIOS 4.6.5

### Các setting cần TẮT

| Setting | Lý do |
|---|---|
| **Above 4G Decoding** | BẮT BUỘC TẮT trên X79  bật sẽ lỗi boot (ngược với desktop Intel gen mới!) |
| Fast Boot | Can thiệp bootloader |
| Secure Boot | Chặn OpenCore |
| VT-d | Gây xung đột IOMMU (hoặc bật quirk `DisableIoMapper`) |
| CSM / Legacy ROM | Cần UEFI thuần |

### Các setting cần BẬT

| Setting | Lý do |
|---|---|
| VT-x | Bắt buộc cho macOS |
| Hyper-Threading | Khai thác đủ 16 luồng |
| Execute Disable Bit | Security, macOS yêu cầu |
| EHCI/XHCI Hand-off | USB trước khi OS nắm quyền |
| SATA Mode: **AHCI** | Nhận ổ cứng đúng |

### CFG Lock

> BIOS Huananzhi X79 không có tuỳ chọn CFG Lock UI  giải quyết bằng quirks:
> - `AppleCpuPmCfgLock = True`
> - `AppleXcpmCfgLock = True`
>
> Nếu muốn unlock thủ công: dùng `ControlMsrE2.efi` qua OpenShell.
> Nguồn: [mokk731  CFG Lock guide](https://github.com/mokk731/X79-E5v2-OpenCore-EFI)

---

## 4. Giai đoạn 3  Map USB từ Windows

> Làm TRƯỚC khi cài macOS. macOS 11.3+ không còn cho phép XhciPortLimit (broken).
> Confirmed: [AwSomeSiz/Atermiter_X79G_Hackintosh](https://github.com/AwSomeSiz/Atermiter_X79G_Hackintosh)  X79 + Polaris dùng USBToolBox.

### Các bước

1. Chạy `Updates/Tools/USBToolBox.exe` (version 0.2)
2. Nhấn `D`  Discover ports
3. Cắm thiết bị USB vào **từng cổng một** (cả USB 2.0 và 3.0)
4. Nhấn `S`  Select ports (tối đa 15 port)
5. Nhấn `K`  Build `UTBMap.kext`
6. Copy vào `EFI/OC/Kexts/`:
   - `USBToolBox.kext`
   - `UTBMap.kext`

> `XhciPortLimit` giữ nguyên `False`  không bao giờ bật.

---

## 5. Giai đoạn 4  Tạo USB cài đặt

### 5.1 Format USB

- Dung lượng: 4GB+
- Format: **FAT32**

### 5.2 Cấu trúc thư mục trên USB

```
USB:\
 com.apple.recovery.boot\
    BaseSystem.dmg
    BaseSystem.chunklist
 EFI\
     BOOT\
        BOOTx64.efi
     OC\
         OpenCore.efi
         config.plist
         ACPI\
            SSDT-EC.aml
            SSDT-PLUG.aml
            SSDT-USBX.aml
         Drivers\
            OpenRuntime.efi     (LoadEarly = True)
            HfsPlusLegacy.efi
            OpenCanopy.efi
         Kexts\
            Lilu.kext
            VirtualSMC.kext
            SMCProcessor.kext
            SMCSuperIO.kext
            WhateverGreen.kext
            AppleALC.kext
            CpuTscSync.kext     (BẮT BUỘC X79)
            RealtekRTL8111.kext
            USBToolBox.kext
            UTBMap.kext         (từ Giai đoạn 3)
         Resources\              (OpenCanopy themes - OcBinaryData)
         Tools\
             OpenShell.efi
```

> Thứ tự kext quan trọng: Lilu  VirtualSMC  SMC plugins  WEG  ALC  CpuTscSync  RTL8111  USBToolBox  UTBMap.
> Dùng ProperTree  `OC Snapshot` để tự động thêm entries sau khi copy xong.

---

## 6. Giai đoạn 5  Edit config.plist

> Bắt đầu từ `Updates/OpenCore_Extracted/Docs/Sample.plist`  KHÔNG edit file cũ.
> Dùng **ProperTree** để edit. Chạy `File  OC Snapshot` sau khi thêm kexts/drivers/SSDTs.
> Script tự động: `configure_opencore.py` trong repo này.

---

### ACPI

| Key | Giá trị cần đặt | Ghi chú |
|---|---|---|
| `ACPI/Add` | Xoá hết 16 entries mẫu. Thêm: `SSDT-EC.aml`, `SSDT-PLUG.aml`, `SSDT-USBX.aml` | `SSDT-PM.aml` thêm sau ở Giai đoạn 7 |
| `ACPI/Delete` | **Clear** (xoá 2 entries Drop CpuPm/Cpu0Ist) | Chỉ Sandy Bridge cần Drop  Ivy Bridge-EP không cần |
| `ACPI/Patch` | **Clear** | Không cần ACPI patch |

---

### Booter

| Key | Default | Đặt thành | Ghi chú |
|---|---|---|---|
| `AvoidRuntimeDefrag` | `False` | **`True`** | KASLR |
| `DevirtualiseMmio` | `False` | **`True`** | X79 + 48GB RAM  MMIO conflict |
| `EnableWriteUnprotector` | `True` | `True` |  |
| `ProvideCustomSlide` | `True` | `True` |  |
| `SetupVirtualMap` | `True` | `True` |  |
| `SyncRuntimePermissions` | `False` | **`True`** | Ivy Bridge |
| `MmioWhitelist` | 2 entries mẫu | **Clear** |  |

> Nguồn: [Dortania  Ivy Bridge-E HEDT Booter Quirks](https://dortania.github.io/OpenCore-Install-Guide/config-HEDT/ivy-bridge-e.html#booter)

---

### DeviceProperties

| Key | Giá trị | Ghi chú |
|---|---|---|
| `PciRoot(0x0)/Pci(0x1b,0x0)/layout-id` | `<01 00 00 00>` | Giữ nguyên  ALC887 layout-id 1 |
| iGPU inject | Không thêm | Xeon E5 v2 không có integrated graphics |
| GPU inject | Không thêm | RX 580 Polaris native, không cần DeviceProperties |

> Path `Pci(0x1b,0x0)` = HDA audio X79 C200 chipset  xác nhận lại bằng Hackintool sau cài.
> Tham khảo: [AwSomeSiz/Atermiter_X79G config.plist](https://github.com/AwSomeSiz/Atermiter_X79G_Hackintosh)  cùng cấu trúc chipset.

---

### Kernel/Add  Thứ tự kext

| # | Kext | Ghi chú |
|---|---|---|
| 1 | `Lilu.kext` | Luôn đầu tiên |
| 2 | `VirtualSMC.kext` | Trước SMC plugins |
| 3 | `SMCProcessor.kext` | CPU sensors |
| 4 | `SMCSuperIO.kext` | Fan sensors |
| 5 | `WhateverGreen.kext` | DRM + GPU |
| 6 | `AppleALC.kext` | Audio ALC887 |
| 7 | `CpuTscSync.kext` | BẮT BUỘC X79 |
| 8 | `RealtekRTL8111.kext` | Ethernet RTL8168 |
| 9 | `USBToolBox.kext` | USB driver |
| 10 | `UTBMap.kext` | USB map |

> Xoá toàn bộ 18 entries mẫu, thêm lại theo thứ tự trên.

### Kernel/Quirks

| Key | Default | Đặt thành | Ghi chú |
|---|---|---|---|
| `AppleCpuPmCfgLock` | `False` | **`True`** | Huananzhi không unlock CFG Lock được |
| `AppleXcpmCfgLock` | `False` | **`True`** | Ivy Bridge-EP |
| `DisableIoMapper` | `False` | **`True`** | Disable VT-d conflicts |
| `DisableLinkeditJettison` | `True` | `True` |  |
| `PanicNoKextDump` | `False` | **`True`** | Debug panic |
| `PowerTimeoutKernelPanic` | `False` | **`True`** | Tránh timeout |
| `XhciPortLimit` | `False` | **`False`** | Dùng UTBMap, không bao giờ bật |
| `LapicKernelPanic` | `False` | `False` | Desktop |

### Kernel/Block, Patch, Force

| Section | Action |
|---|---|
| `Kernel/Block` | **Clear** (xoá 2 entries mẫu) |
| `Kernel/Patch` | **Clear** (xoá 12 entries mẫu) |
| `Kernel/Force` | **Clear** |
| `Kernel/Emulate` | Giữ nguyên  không giả lập CPUID |

---

### Misc/Boot

| Key | Default | Đặt thành | Ghi chú |
|---|---|---|---|
| `LauncherOption` | `'Disabled'` | **`'Full'`** | Đăng ký OC vào BIOS boot entry |
| `PickerMode` | `'Builtin'` | **`'External'`** | OpenCanopy GUI |
| `PickerVariant` | `'Auto'` | `'Acidanthera\GoldenGate'` | Hoặc giữ `'Auto'` |
| `PollAppleHotKeys` | `False` | **`True`** | Cmd+V, Cmd+R, Cmd+S |
| `HideAuxiliary` | `True` | `True` |  |

### Misc/Debug

| Key | Default | Đặt thành | Ghi chú |
|---|---|---|---|
| `AppleDebug` | `False` | **`True`** | Tắt sau khi ổn định |
| `ApplePanic` | `False` | **`True`** | Log panic ra file |
| `DisableWatchDog` | `False` | **`True`** | Tránh timeout khi boot chậm |
| `Target` | `3` | **`67`** | `3 + 64` = serial + file; tắt = đổi lại `3` |

### Misc/Security

| Key | Default | Đặt thành | Ghi chú |
|---|---|---|---|
| `AllowSetDefault` | `False` | **`True`** | Ctrl+Enter đặt default OS |
| `DmgLoading` | `'Signed'` | **`'Any'`** | Recovery image không signed |
| `ScanPolicy` | `17760515` | **`0`** | Scan tất cả |
| `SecureBootModel` | `'Default'` | **`'Disabled'`** | BẮT BUỘC cho OCLP + Ivy Bridge |
| `Vault` | `'Secure'` | **`'Optional'`** | Không dùng vault |

---

### NVRAM

| Key | Default | Đặt thành | Ghi chú |
|---|---|---|---|
| `7C436110.../boot-args` | `-v keepsyms=1` | **`-v keepsyms=1 debug=0x100 npci=0x3000 alcid=1`** | `npci=0x3000` BẮT BUỘC X79 |
| `7C436110.../csr-active-config` | `<00000000>` | **`<03000000>`** | SIP partial cho OCLP |
| `7C436110.../prev-lang:kbd` | `ru-RU:252` | **`en-US:0`** (string) | Ngôn ngữ bàn phím |
| `7C436110.../run-efi-updater` | `'No'` | `'No'` |  |
| `LegacyEnable` | `False` | `False` | BIOS desktop có native NVRAM |
| `WriteFlash` | `True` | `True` |  |

**Về boot-args:**

| Argument | Lý do |
|---|---|
| `-v` | Verbose  hiện log để debug |
| `keepsyms=1` | Ký hiệu debug |
| `debug=0x100` | Ngăn reboot khi panic |
| **`npci=0x3000`** | BẮT BUỘC X79  PCI config issue |
| `alcid=1` | Audio layout-id ALC887 (thử 1  7  11 nếu không ra âm thanh) |

> Sau khi ổn định, xoá: `-v`, `keepsyms=1`, `debug=0x100`

---

### PlatformInfo

> KHÔNG dùng serial mẫu  phải generate riêng để iMessage/FaceTime hoạt động.

**Bước 1**: Chạy [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS)  chọn `MacPro6,1`

**Bước 2**: Điền output vào `PlatformInfo/Generic`:

| Key | Default | Đặt thành |
|---|---|---|
| `SystemProductName` | `'iMac19,1'` | **`'MacPro6,1'`** |
| `SystemSerialNumber` | `'W00000000001'` | **[GenSMBIOS Serial]** |
| `MLB` | `'M0000000000000001'` | **[GenSMBIOS MLB]** |
| `SystemUUID` | `'00000000-...'` | **[GenSMBIOS UUID]** |
| `ROM` | `<112233445566>` | **`<F45C89A5508F>`** (WiFi MAC `F4:5C:89:A5:50:8F`) |

**Bước 3**: Kiểm tra serial tại [checkcoverage.apple.com](https://checkcoverage.apple.com)  phải báo "không tìm thấy".

---

### UEFI

| Key | Default | Đặt thành | Ghi chú |
|---|---|---|---|
| `APFS/MinDate` | `0` | **`-1`** | Cho phép mọi phiên bản APFS |
| `APFS/MinVersion` | `0` | **`-1`** | Cho phép mọi phiên bản APFS |
| `Quirks/ReleaseUsbOwnership` | `False` | **`True`** | EHCI handoff |
| `Quirks/RequestBootVarRouting` | `True` | `True` | Cần cho LauncherOption=Full |
| `Quirks/IgnoreInvalidFlexRatio` | `False` | `False` | Chỉ Sandy Bridge mới cần |
| `Quirks/TscSyncTimeout` | `0` | `0` | Dùng CpuTscSync.kext thay |
| `Quirks/UnblockFsConnect` | `False` | `False` | Không phải HP |

**UEFI/Drivers**  clear hết 47 entries mẫu, thêm lại:

| Driver | LoadEarly | Ghi chú |
|---|---|---|
| `OpenRuntime.efi` | **True** | Bắt buộc |
| `HfsPlusLegacy.efi` | False | Đọc HFS+ |
| `OpenCanopy.efi` | False | GUI picker |

> Không dùng `OpenVariableRuntimeDxe.efi`  BIOS desktop X79 có native NVRAM.

---

## 7. Giai đoạn 6  Cài macOS

### 6.1 Boot từ USB

1. Cắm USB vào cổng **USB 2.0** (tránh USB 3.0 VIA VL805 khi chưa map)
2. Vào BIOS  Boot Menu  chọn USB
3. OpenCore picker  chọn `Install macOS Sequoia`

**Nếu treo/panic ngay:**
- Kiểm tra `npci=0x3000` trong boot-args
- Kiểm tra `CpuTscSync.kext` đã load (Enabled = True trong config.plist)
- Kiểm tra `Above 4G Decoding` TẮT trong BIOS

### 6.2 Disk Utility  Tạo APFS RAID 0

1. Mở Disk Utility  View  **Show All Devices**
2. Chọn cả 2 ổ: Apple SSD SM0128G + Samsung 850 EVO
3. `File  RAID Assistant`  **Striped RAID Set**
4. Format: **APFS** | Name: `Macintosh HD`
5. Tạo  ~240GB volume xuất hiện

### 6.3 Cài đặt

Chọn volume APFS RAID  Continue  đợi ~30 phút, reboot vài lần.  
Mỗi lần reboot: chọn lại `macOS Installer` trong OpenCore picker cho đến khi vào được macOS.

---

## 8. Giai đoạn 7  Post-Install

### 7.1 Copy EFI vào ổ cứng chính

```bash
# Dùng MountEFI (corpnewt/MountEFI) để mount EFI partition
# Copy toàn bộ EFI/ từ USB vào EFI partition của ổ macOS
```

### 7.2 OCLP Root Patch  Bắt buộc cho Ivy Bridge

1. Tải [OpenCore Legacy Patcher 2.4.1](https://github.com/dortania/OpenCore-Legacy-Patcher/releases)
2. Chạy OCLP  **Post-Install Root Patch**
3. Apply patches cho Ivy Bridge CPU PM
4. Reboot

> Cần thiết vì Sequoia đã drop native support cho Ivy Bridge.
> OCLP 2.4.1 confirmed hỗ trợ Sequoia + Ivy Bridge-EP  OCLP changelog Sep 2025.

### 7.3 Tạo SSDT-PM (CPU Power Management tối ưu)

```bash
# Chạy trong macOS Terminal
bash ssdtPRGen.sh-Beta/ssdtPRGen.sh
# Hoặc với thông số cụ thể:
bash ssdtPRGen.sh -p "Xeon E5-2667 v2" -f 3300 -turbo 4000
```

Copy `SSDT-PM.aml` vào `EFI/OC/ACPI/`, thêm entry vào `config.plist/ACPI/Add`, reboot.

### 7.4 Xác nhận USB Map

Mở Hackintool  tab USB  kiểm tra cổng hiện đúng type (USB2/USB3/Internal).  
Nếu sai: chạy lại USBToolBox.exe từ Windows, rebuild UTBMap.kext.

### 7.5 Xác nhận Audio

System Preferences  Sound  Output  phải thấy `Internal Speakers` hoặc `Line Out`.  
Nếu không: thử `alcid=1`  `alcid=7`  `alcid=11`  `alcid=2`.

### 7.6 Tắt Debug sau khi ổn định

```
boot-args: xoá -v, debug=0x100, keepsyms=1
Misc/Debug/Target: 67  3
Misc/Debug/AppleDebug: False
Misc/Debug/ApplePanic: False
```

### 7.7 iMessage / FaceTime

1. Xác nhận ROM = WiFi MAC (`F4:5C:89:A5:50:8F`)
2. Kiểm tra serial tại checkcoverage.apple.com
3. BCM43602 native đảm bảo iMessage hoạt động đầy đủ

### 7.8 Time Machine

Cắm Seagate 1TB  System Preferences  Time Machine  chọn Seagate.  
APFS RAID 0 không có redundancy  backup thường xuyên bắt buộc.

---

## 9. Troubleshooting

| Triệu chứng | Nguyên nhân | Giải pháp |
|---|---|---|
| Màn hình đen (giai đoạn 2) | Thiếu `CpuTscSync.kext` | Thêm kext, Enabled=True |
| Không boot được | Thiếu `npci=0x3000` | Thêm vào boot-args |
| Không boot được | Above 4G Decoding bật | Vào BIOS tắt |
| `OC: Grabbed zero system-id for SB` | SecureBootModel sai | `SecureBootModel = Disabled` |
| Kernel panic | CFG Lock chưa xử lý | `AppleCpuPmCfgLock + AppleXcpmCfgLock = True` |
| Không nhận USB 3.0 | UTBMap.kext chưa có | Chạy lại USBToolBox từ Windows |
| Không có âm thanh | layout-id sai | Thử `alcid=1  7  11  2` |
| WiFi không nhận | BCM43602 lỏng tiếp xúc | Kiểm tra card; thêm `AirportBrcmFixup.kext + brcmfx-driver=2` nếu vẫn không |
| DRM không hoạt động | WEG config | Thêm `unfairgva=1` vào boot-args |
| iMessage không đăng nhập | Serial trùng | Generate lại bằng GenSMBIOS |
| macOS update fail sau OCLP | SIP setting | Giữ `csr-active-config=03000000` |

---

## 10. Tham khảo & Nguồn

### Repos X79 Huananzhi  Gần với cấu hình này nhất

| Repo | CPU | GPU | Board | macOS | Điểm tương đồng |
|---|---|---|---|---|---|
| [nguyenphucdev/OpenCore_X79_X99_Xeon_E5_2650v2](https://github.com/nguyenphucdev/OpenCore_X79_X99_Xeon_E5_2650v2) | E5-2650 v2 | RX 470 | X79/X99 | Catalina |  Người Việt, Ivy Bridge-EP + Polaris |
| [antipeth/EFI-Motherboard-X79-OpenCore-Hackintosh](https://github.com/antipeth/EFI-Motherboard-X79-OpenCore-Hackintosh) | E5-2450 v2 | HD 7750 | **Huananzhi X79** | Monterey | Chính xác cùng mainboard Huananzhi |
| [AwSomeSiz/Atermiter_X79G_Hackintosh](https://github.com/AwSomeSiz/Atermiter_X79G_Hackintosh) | E5-1650 v2 | **RX 570** | Atermiter X79G | Big SurVentura | Cùng Polaris GPU, ACPI đầy đủ, có Release |
| [mokk731/X79-E5v2-OpenCore-EFI](https://github.com/mokk731/X79-E5v2-OpenCore-EFI) | E5-2650 v2 | GTX 650 | X79-H67 | Catalina | Ghi chép chi tiết, CFG Lock guide, cập nhật 2025 |
| [maklakowiktor/EFI-X79-HUANANZHI-ZD3-INTEL-XEON-E5-2640-V1-RX570-4GB](https://github.com/maklakowiktor/EFI-X79-HUANANZHI-ZD3-INTEL-XEON-E5-2640-V1-RX570-4GB) | E5-2640 v1 | **RX 570** | **Huananzhi ZD3** | Big Sur | Huananzhi + Polaris, confirmed hoạt động |
| [cchs29/Hackintosh-huanan-X79-2650-k600-opencore-bigsur](https://github.com/cchs29/Hackintosh-huanan-X79-2650-k600-opencore-bigsur) | E5-2650 | Quadro K600 | Huananzhi X79 | Big Sur | Chính xác board Huananzhi |
| [xdien/hackintosh-x79-dual](https://github.com/xdien/hackintosh-x79-dual) | E5-2620 v2 |  | Huananzhi X79 |  |  Người Việt, dual socket |

### Hướng dẫn chính thức

| Link | Nội dung |
|---|---|
| [Dortania  Ivy Bridge-E HEDT Guide](https://dortania.github.io/OpenCore-Install-Guide/config-HEDT/ivy-bridge-e.html) | **Hướng dẫn chính** cho build này |
| [Dortania  Getting Started With ACPI](https://dortania.github.io/Getting-Started-With-ACPI/) | Tạo/tải SSDTs |
| [Dortania  GPU Buyers Guide](https://dortania.github.io/GPU-Buyers-Guide/) | Xác nhận RX 580 support |
| [OpenCore Legacy Patcher Docs](https://dortania.github.io/OpenCore-Legacy-Patcher/) | OCLP post-install |

### Kexts & Tools

| Link | Nội dung |
|---|---|
| [acidanthera/OpenCorePkg](https://github.com/acidanthera/OpenCorePkg/releases) | OpenCore 1.0.6 |
| [acidanthera/CpuTscSync](https://github.com/acidanthera/CpuTscSync) | TSC sync  BẮT BUỘC X79 |
| [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X) | Realtek RTL8168 kext |
| [USBToolBox/tool](https://github.com/USBToolBox/tool) | USB mapping từ Windows |
| [corpnewt/GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) | Generate MacPro6,1 serial |
| [corpnewt/ProperTree](https://github.com/corpnewt/ProperTree) | plist editor |
| [benbaker76/Hackintool](https://github.com/benbaker76/Hackintool/releases) | PCIe/USB/Audio verify |

### Script trong repo này

| File | Mục đích |
|---|---|
| `configure_opencore.py` | Tự động tạo config.plist từ Sample.plist |
| `ssdtPRGen.sh-Beta/ssdtPRGen.sh` | Tạo SSDT-PM.aml sau cài |
| `Guides/Tham_Khao_GitHub_X79.md` | Chi tiết tổng hợp repos tham khảo |
