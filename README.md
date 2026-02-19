# Hackintosh Desktop: Xeon E5-2667 v2 + RX 580 (Huananzhi X79)

> **Ngôn ngữ**: Tiếng Việt | **Cập nhật lần cuối**: 2025

---

## Cấu hình máy (Đã xác nhận qua WMI scan)

| Thành phần     | Chi tiết                                                                        | Ghi chú                          |
|----------------|---------------------------------------------------------------------------------|----------------------------------|
| **CPU**        | Intel Xeon E5-2667 v2 @ 3.30GHz — Ivy Bridge-EP, 8C/16T, L3 25MB              | LGA2011, socket X79              |
| **Mainboard**  | **HUANANZHI X79** — C200/C600 Chipset, Intel Q65 LPC (`DEV_1C4C`), V2.49PB     | AMI BIOS 4.6.5                   |
| **GPU**        | AMD Radeon RX 580 Series (Polaris, 4GB, `DEV_67DF`)                            | Hỗ trợ native từ High Sierra+    |
| **RAM**        | 48 GB Samsung DDR3 ECC 1333MHz — 4 DIMM (16GB×2 + 8GB×2)                       | Samsung M393 series (server ECC) |
| **WiFi**       | **Broadcom BCM43602** — `VEN_14E4 DEV_43BA SUBSYS_0133106B` (subsys 106B=Apple)| ✅ Native macOS, KHÔNG cần kext  |
| **Bluetooth**  | Apple Broadcom Built-in BT — `USB\VID_05AC PID_8290`                           | ✅ Native macOS, KHÔNG cần kext  |
| **Ethernet**   | **Realtek RTL8168/RTL8111** — `PCI\VEN_10EC DEV_8168`                          | Cần `RealtekRTL8111.kext`        |
| **Audio**      | **Realtek ALC887** — `HDAUDIO\VEN_10EC DEV_0887` + AMD HDMI (RX 580)           | AppleALC layout-id: **1** hoặc **7** |
| **USB 2.0**    | Intel 6 Series/C200 EHCI — `DEV_1C26` + `DEV_1C2D`                            | 2 controller                     |
| **USB 3.0**    | **VIA VL805** — `VEN_1106 DEV_3483`                                            | Cần USB mapping sau cài           |
| **Ổ cứng (macOS)** | **Apple SSD SM0128G 128GB** (SATA)                                         | ✅ Hỗ trợ native, không cần kext |
| **Ổ cứng (Win)** | SK Hynix HFS256G32MND 256GB (SATA)                                           | Boot Windows                     |
| **Ổ cứng khác** | Samsung 850 EVO 120GB + Seagate 1TB HDD                                       | Backup / Time Machine / Dữ liệu  |

---

## macOS Target

**macOS Sequoia 15.x** thông qua OpenCore + OCLP

> - RX 580 (Polaris) hỗ trợ native từ High Sierra đến Sequoia — không cần patch GPU.
> - CPU Ivy Bridge cần **OCLP Root Patch** sau khi cài để kích hoạt full Power Management.
> - Ivy Bridge + Sequoia 15.7.x đã được xác nhận hoạt động (nguồn: Reddit r/hackintosh, 2026).
> - OCLP 2.4.1 (Sep 2025) hỗ trợ ổn định Sequoia + Ivy Bridge.

## SMBIOS

**`MacPro6,1`** — Mac Pro Late 2013, CPU Ivy Bridge-EP Xeon (cùng kiến trúc với E5-2667 v2).

> Tạo serial mới bằng [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS), chọn `MacPro6,1`.  
> **KHÔNG dùng serial có sẵn** — phải generate của riêng mình để tránh xung đột iMessage/FaceTime.

## OpenCore Version

**1.0.6**

## Phiên bản Binary

| Binary                  | Phiên bản | Nguồn                                 |
|-------------------------|-----------|---------------------------------------|
| OpenCore                | 1.0.6     | acidanthera/OpenCorePkg               |
| Lilu                    | 1.7.1     | acidanthera/Lilu                      |
| WhateverGreen           | 1.7.0     | acidanthera/WhateverGreen             |
| AppleALC                | 1.9.6     | acidanthera/AppleALC                  |
| VirtualSMC              | 1.3.7     | acidanthera/VirtualSMC                |
| RealtekRTL8111          | v3.0.0    | Mieze/RTL8111_driver_for_OS_X         |
| CpuTscSync              | 1.1.2     | acidanthera/CpuTscSync                |

---

## Kexts cần thiết

### Bắt buộc (Core)

| Kext                   | Mục đích                                                      | Trạng thái     |
|------------------------|---------------------------------------------------------------|----------------|
| `Lilu.kext`            | Patcher lõi — **nạp đầu tiên**                                | ✅ Đã tải      |
| `VirtualSMC.kext`      | Giả lập SMC Apple                                             | ✅ Đã tải      |
| `WhateverGreen.kext`   | GPU / DRM patch (cần ngay cả với RX 580)                      | ✅ Đã tải      |
| `AppleALC.kext`        | Âm thanh onboard (**ALC887** — layout-id: `1` hoặc `7`)      | ✅ Đã tải      |
| `SMCProcessor.kext`    | Nhiệt độ / công suất CPU (trong gói VirtualSMC)               | ✅ Có trong gói|
| `SMCSuperIO.kext`      | Quạt / cảm biến phần cứng (trong gói VirtualSMC)             | ✅ Có trong gói|

### ⚠️ Bắt buộc cho X79 (khác desktop thường)

| Kext                   | Mục đích                                                      | Trạng thái        |
|------------------------|---------------------------------------------------------------|-------------------|
| `CpuTscSync.kext`      | **Đồng bộ TSC giữa các core — THIẾU SẼ TREO CHẮC CHẮN**      | ✅ Đã tải        |

### Mạng

| Kext                   | Mục đích                                                      | Trạng thái        |
|------------------------|---------------------------------------------------------------|-------------------|
| `RealtekRTL8111.kext`  | Realtek RTL8168/8111 Ethernet (`VEN_10EC&DEV_8168`)           | ✅ Đã tải       |

> **Không cần** WiFi kext — BCM43602 được macOS hỗ trợ native hoàn toàn (AirDrop, Handoff, Continuity).  
> **Không cần** BT kext — Apple BCM `VID_05AC&PID_8290` native.  
> **Không cần** `IntelMausi` — máy dùng Realtek, không phải Intel NIC.  
> **Không cần** `NVMeFix` — Apple SSD SM0128G là SATA, không phải NVMe.

---

## Drivers (EFI/OC/Drivers)

| Driver                       | Mục đích                                  | Ghi chú              |
|------------------------------|-------------------------------------------|----------------------|
| `OpenRuntime.efi`            | Bắt buộc — fix memory/boot               | Luôn cần             |
| `HfsPlusLegacy.efi`          | Hỗ trợ phân vùng HFS+                    | Cần cho installer    |
| `OpenCanopy.efi`             | GUI boot picker (đẹp hơn)                | Tuỳ chọn             |

> **Không cần** `OpenVariableRuntimeDxe.efi` — BIOS desktop hỗ trợ NVRAM native.

---

## ACPI Files cần thiết

| File                   | Mục đích                                                      | Ghi chú                          |
|------------------------|---------------------------------------------------------------|----------------------------------|
| `SSDT-PM.aml`          | CPU Power Management                                          | Tạo bằng `ssdtPRGen.sh` sau boot |
| `SSDT-EC.aml`          | Embedded Controller giả (dummy)                               | Cần cho Catalina+                |
| `SSDT-USBX.aml`        | USB power injection                                           | Cần cho USB 3.0 đúng             |
| `SSDT-PLUG.aml`        | Plugin Type cho XCPM                                          | Ivy Bridge-EP Xeon cần           |
| `SSDT-RTC0-RANGE.aml`  | Fix RTC                                                       | Một số bo X79 cần                |

> `SSDT-IMEI.aml` **không cần** — chipset X79 C600/C200 native, khác H67/P67 6-series.  
> Dùng `../ssdtPRGen.sh-Beta/ssdtPRGen.sh` để tạo `SSDT-PM.aml` sau boot lần đầu.

---

## Cài đặt BIOS (Huananzhi X79 AMI BIOS 4.6.5)

### TẮT

| Setting                | Lý do                                                         |
|------------------------|---------------------------------------------------------------|
| **Above 4G Decoding**  | ⚠️ **BẮT BUỘC TẮT trên X79** — bật sẽ lỗi boot (khác desktop thông thường!) |
| Fast Boot              | Can thiệp quá trình khởi động                                 |
| Secure Boot            | Chặn OpenCore                                                 |
| VT-d                   | Gây xung đột IOMMU (hoặc bật `DisableIoMapper` = YES)        |
| CSM / Legacy ROM       | Cần UEFI thuần                                                |

### BẬT

| Setting                | Lý do                                                         |
|------------------------|---------------------------------------------------------------|
| VT-x                   | Bắt buộc cho macOS                                            |
| Hyper-Threading        | Khai thác đủ 16 luồng                                         |
| Execute Disable Bit    | Bảo mật, macOS yêu cầu                                        |
| EHCI/XHCI Hand-off     | USB trước khi OS nắm quyền                                    |
| SATA Mode: AHCI        | Nhận ổ cứng đúng                                              |

### Về CFG Lock

> BIOS Huananzhi X79 thường **không có tuỳ chọn CFG Lock** — giải quyết bằng quirks:
> - `Kernel → Quirks → AppleCpuPmCfgLock = YES`
> - `Kernel → Quirks → AppleXcpmCfgLock = YES`

---

## Boot Arguments bắt buộc

```
boot-args: -v keepsyms=1 debug=0x100 npci=0x3000 alcid=1
```

| Argument         | Lý do                                                              |
|------------------|--------------------------------------------------------------------|
| `-v`             | Verbose mode — hiện log để debug                                   |
| `keepsyms=1`     | Giữ ký hiệu cho debug                                              |
| `debug=0x100`    | Ngăn reboot khi panic                                              |
| **`npci=0x3000`**| ⚠️ **BẮT BUỘC trên X79** — fix PCI configuration issue           |
| `alcid=1`        | Audio layout-id cho ALC887 (thử 1, nếu không dùng 7 hoặc 11)     |

> Sau khi hệ thống ổn định, xoá `-v`, `keepsyms=1`, `debug=0x100` để khởi động bình thường.

---

## GPU: AMD Radeon RX 580 (Polaris) — Cấu hình chi tiết

```
PCI\VEN_1002&DEV_67DF — AMD Radeon RX 580 Series (Polaris 10)
HDAUDIO\VEN_1002&DEV_AA01 — AMD High Definition Audio (HDMI/DP audio)
```

### Hỗ trợ native — KHÔNG cần patch GPU

RX 580 (Polaris) được macOS hỗ trợ **hoàn toàn native** từ High Sierra đến Sequoia.  
Không cần `DeviceProperties` patch, không cần frame buffer injection, không cần kext GPU riêng.

### WhateverGreen.kext — Vẫn cần

Dù RX 580 là native, `WhateverGreen.kext` vẫn cần thiết vì:
- Fix DRM (Netflix, Apple TV+, Amazon Prime trong Safari)
- Fix HDMI/DisplayPort audio sync
- Fix một số vấn đề khởi động với AMD GPU trên non-Apple hardware

### Không có iGPU — Quan trọng cho config.plist

CPU Xeon E5-2667 v2 **không có integrated graphics** — toàn bộ output đi qua RX 580.  
Do đó cần đảm bảo:

| Setting | Giá trị | Lý do |
|---|---|---|
| `DeviceProperties → iGPU` | ❌ Không thêm | Không có iGPU để inject |
| `AAPL,ig-platform-id` | ❌ Không đặt | Chỉ dùng cho Intel iGPU |
| `Misc → Boot → PickerMode` | `Builtin` hoặc `External` | Đảm bảo picker hiện trên dGPU |
| `NVRAM → boot-args` | Không cần `igfxonln=1` | Không có iGPU |

### Boot-arg GPU (không cần cho Polaris)

| Boot-arg | GPU | Có cần không |
|---|---|--|
| `agdpmod=pikera` | Navi (RX 5000/6000/7000) | ❌ **Không cần** cho RX 580 |
| `radpg=15` | Polaris cũ (RX 4xx) | ❌ Thường không cần RX 580 |
| `-wegnoegpu` | Disable iGPU | ❌ Không áp dụng (không có iGPU) |
| `unfairgva=1` | Fix DRM hardware accel | ✅ Thêm nếu DRM không hoạt động |

> **Kết luận**: Không cần bất kỳ boot-arg GPU nào cho RX 580 trên build này.

### PCIe Path của GPU

Trên X79, GPU thường cắm slot PCIe x16 chính — path thường là:
```
PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)
```
Xác nhận path thực tế bằng **Hackintool** sau khi cài (tab PCIe).

### HDMI Audio từ RX 580

AMD HDMI audio (`VEN_1002&DEV_AA01`) hoạt động native qua HDMI/DisplayPort.  
Không cần cấu hình thêm — hoạt động song song với ALC887 onboard.

---

## Phần cứng WiFi & Bluetooth — Chi tiết quan trọng

### WiFi: Broadcom BCM43602 (Apple OEM)

```
PCI\VEN_14E4&DEV_43BA&SUBSYS_0133106B&REV_01
```

- `VEN_14E4` = Broadcom, `DEV_43BA` = BCM43602, `SUBSYS_106B` = **Apple vendor** — đây là card Apple OEM
- macOS nhận diện native hoàn toàn **không cần bất kỳ kext nào**
- Hỗ trợ đầy đủ: AirDrop, Handoff, Continuity, AirPlay Receiver, iMessage, FaceTime
- Đây là card Apple dùng trong MacBook Pro 2015-2017 và iMac 2015

> ✅ **Không cần** AirportItlwm, itlwm, AirportBrcmFixup, hoặc bất kỳ WiFi kext nào.

### Bluetooth: Apple Broadcom Built-in

```
USB\VID_05AC&PID_8290
```

- `VID_05AC` = Apple vendor ID — đây là thiết bị BT Apple chính hãng
- Native macOS support, không cần kext, Bluetooth 4.0+
- BT và WiFi chia sẻ MAC address (F4:5C:89:A5:50:8F / :90)

> ✅ **Không cần** BrcmPatchRAM, BrcmFirmwareData, hoặc bất kỳ BT kext nào.

---

## Audio: Realtek ALC887

```
HDAUDIO\FUNC_01&VEN_10EC&DEV_0887&SUBSYS_10EC0887
```

| layout-id | Kết quả thường gặp                                              |
|-----------|-----------------------------------------------------------------|
| `1`       | Khuyến nghị thử trước — hỗ trợ Line Out + Headphone            |
| `7`       | Thử nếu layout 1 không ra âm thanh                             |
| `11`      | Thử nếu cần mic input                                           |
| `2`       | Thay thế cuối cùng                                              |

> Thiết lập trong `boot-args`: `alcid=1` (đổi số sau `alcid=` để thử layout khác).

---

## USB Controllers & Mapping

| Controller                               | DeviceID              | Loại     | Ghi chú                       |
|------------------------------------------|-----------------------|----------|---------------------------------|
| Intel 6 Series/C200 EHCI (`DEV_1C26`)   | `PCI\VEN_8086&DEV_1C26` | USB 2.0 | Controller thứ nhất           |
| Intel 6 Series/C200 EHCI (`DEV_1C2D`)   | `PCI\VEN_8086&DEV_1C2D` | USB 2.0 | Controller thứ hai            |
| **VIA VL805** (`DEV_3483`)               | `PCI\VEN_1106&DEV_3483` | USB 3.0 | Card PCIe thêm vào            |

> **Map USB từ Windows TRƯỚC khi cài macOS** bằng [USBToolBox](https://github.com/USBToolBox/tool):  
> 1. Tải `Windows.exe` từ releases, chạy trong Windows  
> 2. Cắm thiết bị USB vào từng cổng để discover  
> 3. Nhấn `K` để build `UTBMap.kext`  
> 4. Copy `UTBMap.kext` + `USBToolBox.kext` vào `EFI/OC/Kexts/` **trước khi boot installer**  
>
> ✅ **Không cần `XhciPortLimit`** — USBToolBox map từ Windows nên không bao giờ cần quirk này (bị broken từ macOS 11.3+).

---

## Ổ cứng

| Ổ cứng                         | Model                    | Dung lượng | Mục đích                      | Interface |
|--------------------------------|--------------------------|------------|-------------------------------|----------|
| **Apple SSD SM0128G**          | Apple OEM SATA SSD       | 128 GB     | **macOS RAID 0** (1/2) ✅      | SATA      |
| **Samsung 850 EVO 120GB**      | Samsung SATA SSD         | 120 GB     | **macOS RAID 0** (2/2) ✅      | SATA      |
| SK Hynix HFS256G32MND          | SK Hynix SATA SSD        | 256 GB     | Boot Windows                  | SATA      |
| Seagate ST1000LM024            | HDD 5400rpm              | 1 TB       | Dữ liệu chung / Time Machine   | SATA      |

### Kế hoạch APFS RAID 0 (Stripe) cho macOS

> Gộp **Apple SSD 128GB + Samsung 850 EVO 120GB** thành 1 volume **~240GB** cho macOS.
> Chấp nhận mất ~8GB lẻ do cận aligned với ổ nhỏ hơn (120GB).

**Lý do chọn APFS RAID 0 thay vì Fusion Drive:**
- Fusion Drive (CoreStorage) thiết kế cho cặp SSD + HDD, không tối ưu cho 2 SSD
- APFS RAID 0 native trên macOS 10.14+, hỗ trợ đầy đủ TRIM, nén, mã hoá, snapshot
- OpenCore boot từ APFS RAID volume được hỗ trợ đầy đủ

**Các bước tạo APFS RAID 0 (chạy trong macOS sau khi cài xong vào1 ổ):**

```bash
# Bước 1: Xác định disk identifier của 2 ổ
diskutil list
# Tìm: Apple SSD SM0128G và Samsung 850 EVO 120GB
# Giả sử là disk0 (Apple 128GB) và disk2 (Samsung 120GB)

# Bước 2: Tạo APFS RAID 0 Stripe Set
sudo diskutil apfs createRAID set "Macintosh HD" APFS-Stripe disk0 disk2

# KẾT QUẢ: 1 volume APFS ~240GB xuất hiện
# Cài đặt bình thường lên RAID volume này
```

> ⚠️ **Thứ tự thực hiện:**
> 1. Cài macOS vào **Apple SSD SM0128G** trước (single drive)
> 2. Boot vào macOS, mở Terminal
> 3. Chạy lệnh `diskutil apfs createRAID` ở trên
> 4. macOS sẽ hỏi migrate data sang RAID volume mới
> 5. Cập nhật EFI boot entry nếu cần (OpenCore tự nhận APFS RAID)

> ✅ APFS RAID 0 hỗ trợ **APFS snapshot** (Time Machine), **FileVault 2**, và **TRIM** trên cả 2 ổ.

**So sánh các phương án:**

| Phương án | Dung lượng | Hiệu năng | Redundancy | Ghi chú |
|---|---|---|---|---|
| **APFS RAID 0 Stripe** | ~240 GB | ⬆️ Read+Write nhanh x2 | ❌ Không | **Ư u tiên** |
| Chỉ dùng Apple SSD | 128 GB | Bình thường | n/a | Ưu tiên 2 |
| Fusion Drive (CoreStorage) | ~240 GB | SSD cache cho HDD | ❌ Không | Cho SSD+HDD, không tối ưu |

---

## Các bước cài đặt

### 1. Tải bộ cài macOS Sequoia

```powershell
# Board ID chính xác cho Sequoia 15:
cd "f:\VScode\Hackintosh\Xeon-E5-2667v2-OpenCore\_tmp\sequoia_recovery"
# Hoặc dùng đường dẫn đện macrecovery:
$pythonExe = "C:\Users\Phi\AppData\Local\Programs\Python\Python311\python.exe"
$macrecovery = "f:\VScode\Hackintosh\X220-OpenCore\Updates\OpenCore_Extracted\Utilities\macrecovery\macrecovery.py"
& $pythonExe $macrecovery -b Mac-937A206F2EE63C01 -m 00000000000000000 download
```

Sau khi tải xong sẽ có file `BaseSystem.dmg` + `BaseSystem.chunklist` trong thư mục chạy lệnh.

Tạo USB format FAT32, tạo folder `\com.apple.recovery.boot\` và copy file `.dmg` + `.chunklist` vào.

### 2. Chuẩn bị EFI

1. Copy thư mục `EFI/` vào USB
2. Copy kexts từ `Kexts/Extracted/` vào `EFI/OC/Kexts/`:
   - `Lilu.kext`
   - `VirtualSMC.kext`, `SMCProcessor.kext`, `SMCSuperIO.kext`
   - `WhateverGreen.kext`
   - `AppleALC.kext`
   - `RealtekRTL8111.kext` ← Ethernet
   - `CpuTscSync.kext` ← **BẮT BUỘC X79**
3. Chạy `configure_opencore.py` để tạo `config.plist` tự động
4. **Generate SMBIOS mới** bằng GenSMBIOS (`MacPro6,1`), điền vào `PlatformInfo → Generic`

### 3. Cài đặt macOS

Boot từ USB → chọn `Install macOS Sequoia` → cài vào **Apple SSD SM0128G 128GB**.

### 4. Post-Install

1. **OCLP**: Tải [OpenCore Legacy Patcher](https://github.com/dortania/OpenCore-Legacy-Patcher/releases) → Post-Install Root Patch → patch Ivy Bridge CPU PM
2. **SSDT-PM**: Tạo `SSDT-PM.aml` bằng `ssdtPRGen.sh` để tối ưu power management
3. **USB Map**: Đã map từ Windows trước khi cài — xác nhận `UTBMap.kext` + `USBToolBox.kext` đang load đúng
4. **Hackintool**: Xác nhận PCIe paths, USB ports, audio layout

---

## Key config.plist — So sánh với X220

| Setting                              | X220 (Sandy Bridge Laptop) | Build này (Ivy Bridge-EP Desktop) |
|--------------------------------------|----------------------------|------------------------------------|
| SMBIOS                               | `MacBookPro8,1`            | `MacPro6,1`                        |
| `AAPL,snb-platform-id`              | `00 00 01 00`              | ❌ Không cần (không có iGPU)        |
| DeviceProperties (GPU)               | Intel HD 3000 patches       | ❌ Không cần (RX 580 native)       |
| NVRAM Emulation                      | ✅ Cần                      | ❌ Không cần (BIOS native NVRAM)   |
| `IgnoreInvalidFlexRatio`            | ✅ YES (Sandy Bridge)       | ❌ NO                               |
| `AppleCpuPmCfgLock`                 | ✅ YES                      | ✅ YES (Huananzhi X79 không unlock) |
| `AppleXcpmCfgLock`                  | ❌ NO                       | ✅ YES                              |
| `DisableIoMapper`                   | ✅ YES                      | ✅ YES                              |
| `XhciPortLimit`                     | ❌ NO                       | ❌ **KHÔNG CẦN** (dùng USBToolBox từ Windows) |
| VoodooPS2 / Battery kexts           | ✅ Cần                      | ❌ Không cần (desktop)             |
| **`CpuTscSync.kext`**               | ❌ Không cần                | ✅ **BẮT BUỘC** (X79 multi-core)   |
| Boot-arg `npci=0x3000`              | ❌ Không cần                | ✅ **BẮT BUỘC** (X79)              |
| **Above 4G Decoding**               | Bật                         | ⚠️ **TẮT** (X79 đặc thù)          |

---

## Ghi chú & Troubleshooting

### Treo ở giai đoạn 2 (màn hình đen)
→ Thiếu `CpuTscSync.kext` hoặc thiếu `npci=0x3000` trong boot-args.

### Không nhận USB 3.0
→ Kiểm tra `UTBMap.kext` + `USBToolBox.kext` đã có trong `EFI/OC/Kexts/` và được enable trong `config.plist`.  
→ Nếu chưa map: chạy [USBToolBox](https://github.com/USBToolBox/tool) từ **Windows** để tạo map, **không bật `XhciPortLimit`** (broken từ macOS 11.3+).

### Lỗi "OC: Grabbed zero system-id for SB"
→ `Misc → Security → SecureBootModel → Disabled`

### Panic / crash khi boot
→ Thêm `-v keepsyms=1 debug=0x100` vào boot-args để xem log đầy đủ.

### Không có âm thanh
→ Thử lần lượt: `alcid=1`, `alcid=7`, `alcid=11`, `alcid=2`.

### WiFi không thấy mạng
→ Kiểm tra card BCM43602 đã cắm chặt; đây là card native không cần kext. Nếu vẫn không nhận, thêm `AirportBrcmFixup.kext` và boot-arg `brcmfx-driver=2`.

---

## config.plist — Tất cả thay đổi so với Sample.plist gốc (OC 1.0.6)

> Dùng `configure_opencore.py` để tự động áp dụng. Bảng bên dưới là reference thủ công.  
> Ký hiệu: ✏️ = phải đổi | ✅ = giữ nguyên default | ➕ = thêm mới | 🗑️ = xoá/clear

---

### ACPI

| Đường dẫn | Default (Sample) | Giá trị cho build này | Ghi chú |
|---|---|---|---|
| `ACPI/Add` | 16 entries (nhiều platform) | ✏️ Xoá hết, thêm chỉ: `SSDT-EC.aml`, `SSDT-PLUG.aml`, `SSDT-USBX.aml` | `SSDT-PM.aml` thêm sau khi cài |
| `ACPI/Delete` | 2 entries (Drop CpuPm, Cpu0Ist) | ✏️ **Xoá hết** — Enabled = False hoặc clear list | Chỉ Sandy Bridge mới cần Drop; Ivy Bridge-EP không cần |
| `ACPI/Patch` | 3 entries mẫu | ✏️ Clear (để `[]`) | Không cần ACPI patch cho X79 |
| `ACPI/Quirks/ResetLogoStatus` | `True` | ✅ Giữ | — |
| Các Quirks ACPI còn lại | `False` | ✅ Giữ | — |

---

### Booter

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `Booter/Quirks/AvoidRuntimeDefrag` | `False` | ✏️ **`True`** | Cần cho KASLR hoạt động |
| `Booter/Quirks/DevirtualiseMmio` | `False` | ✏️ **`True`** | X79 + 48GB RAM cần để tránh conflict MMIO |
| `Booter/Quirks/EnableSafeModeSlide` | `True` | ✅ Giữ | — |
| `Booter/Quirks/EnableWriteUnprotector` | `True` | ✅ Giữ | — |
| `Booter/Quirks/FixupAppleEfiImages` | `True` | ✅ Giữ | — |
| `Booter/Quirks/ProvideCustomSlide` | `True` | ✅ Giữ | — |
| `Booter/Quirks/SetupVirtualMap` | `True` | ✅ Giữ | — |
| `Booter/Quirks/SyncRuntimePermissions` | `False` | ✏️ **`True`** | Cần cho Ivy Bridge |
| `Booter/Quirks/ResizeAppleGpuBars` | `-1` | ✅ Giữ | RX 580 không cần Resizable BAR |
| `Booter/MmioWhitelist` | 2 entries mẫu | ✏️ Clear (để `[]`) | Chỉ cần khi DevirtualiseMmio gặp lỗi |

---

### DeviceProperties

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `DeviceProperties/Add/PciRoot(0x0)/Pci(0x1b,0x0)/layout-id` | `<01 00 00 00>` | ✅ Giữ (layout-id = 1) | ALC887 — thử 1 trước, nếu không âm thanh đổi sang `<07 00 00 00>` |
| GPU DeviceProperties | _(không có trong Sample)_ | ✅ Không thêm | RX 580 native, không cần inject |
| Ethernet DeviceProperties | _(không có)_ | ➕ Tuỳ chọn: `built-in = <01>` tại path RTL8168 | Xác nhận PCIe path bằng Hackintool trước |

> **Note**: Path `PciRoot(0x0)/Pci(0x1b,0x0)` là path audio chuẩn của X79 C200 chipset — `DEV_1C26/1C2D` EHCI ở `0x1c`, audio HDA ở `0x1b`. Xác nhận lại bằng Hackintool sau cài.

---

### Kernel

#### Kernel/Add — Kext list

| Kext | Thứ tự | Ghi chú |
|---|---|---|
| `Lilu.kext` | 1 | Luôn đầu tiên |
| `VirtualSMC.kext` | 2 | Trước SMC plugins |
| `SMCProcessor.kext` | 3 | CPU sensors |
| `SMCSuperIO.kext` | 3 | Fan sensors |
| `WhateverGreen.kext` | 4 | DRM + GPU |
| `AppleALC.kext` | 5 | Audio ALC887 |
| `CpuTscSync.kext` | 6 | **BẮT BUỘC X79** |
| `RealtekRTL8111.kext` | 7 | Ethernet RTL8168 |
| `USBToolBox.kext` | 8 | USB driver |
| `UTBMap.kext` | 9 | USB map (tạo từ USBToolBox.exe) |

> Xoá toàn bộ 18 entries mẫu trong Sample/Add, thêm lại theo list trên.

#### Kernel/Quirks

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `AppleCpuPmCfgLock` | `False` | ✏️ **`True`** | BIOS Huananzhi X79 không unlock CFG Lock |
| `AppleXcpmCfgLock` | `False` | ✏️ **`True`** | Ivy Bridge-EP cần |
| `AppleXcpmExtraMsrs` | `False` | ✅ Giữ | — |
| `DisableIoMapper` | `False` | ✏️ **`True`** | Disable VT-d IOMMU conflicts |
| `DisableIoMapperMapping` | `False` | ✅ Giữ | — |
| `DisableLinkeditJettison` | `True` | ✅ Giữ | — |
| `LapicKernelPanic` | `False` | ✅ Giữ | Không cần cho desktop |
| `PanicNoKextDump` | `False` | ✏️ **`True`** | Dễ debug panic |
| `PowerTimeoutKernelPanic` | `False` | ✏️ **`True`** | Tránh timeout panic |
| `ProvideCurrentCpuInfo` | `False` | ✅ Giữ | — |
| `SetApfsTrimTimeout` | `-1` | ✅ Giữ | SATA SSD dùng -1 |
| `ThirdPartyDrives` | `False` | ✅ Giữ | Samsung 850 EVO + Apple SSD đều không cần |
| `XhciPortLimit` | `False` | ✅ Giữ False | Đang dùng USBToolBox map |

#### Kernel/Block, Patch, Force, Emulate

| Phần | Action |
|---|---|
| `Kernel/Block` | ✏️ Clear (xoá 2 entries mẫu) |
| `Kernel/Patch` | ✏️ Clear (xoá 12 entries mẫu) — không cần patch kernel cho X79 |
| `Kernel/Force` | ✏️ Clear |
| `Kernel/Emulate` | ✅ Giữ nguyên (tất cả empty/False) — không giả lập CPUID |

---

### Misc

#### Misc/Boot

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `HideAuxiliary` | `True` | ✅ Giữ | — |
| `LauncherOption` | `'Disabled'` | ✏️ **`'Full'`** | Đăng ký OC vào BIOS boot menu |
| `PickerMode` | `'Builtin'` | ✏️ **`'External'`** | Dùng OpenCanopy GUI |
| `PickerVariant` | `'Auto'` | ✏️ **`'Acidanthera\\GoldenGate'`** | Theme đẹp, hoặc để `'Auto'` |
| `PollAppleHotKeys` | `False` | ✏️ **`True`** | Cmd+V, Cmd+R, Cmd+S |
| `ShowPicker` | `True` | ✅ Giữ | — |
| `Timeout` | `5` | ✅ Giữ | — |

#### Misc/Debug

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `AppleDebug` | `False` | ✏️ **`True`** | Bật để debug (tắt sau khi ổn định) |
| `ApplePanic` | `False` | ✏️ **`True`** | Log panic (tắt sau khi ổn định) |
| `DisableWatchDog` | `False` | ✏️ **`True`** | Tránh timeout khi boot chậm |
| `Target` | `3` | ✏️ **`67`** | `3` (serial) + `64` (file) = 67; tắt = `3` |

#### Misc/Security

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `AllowSetDefault` | `False` | ✏️ **`True`** | Ctrl+Enter để đặt default OS |
| `BlacklistAppleUpdate` | `True` | ✅ Giữ | — |
| `DmgLoading` | `'Signed'` | ✏️ **`'Any'`** | Recovery image không signed |
| `ScanPolicy` | `17760515` | ✏️ **`0`** | Scan tất cả, không filter |
| `SecureBootModel` | `'Default'` | ✏️ **`'Disabled'`** | **BẮT BUỘC** cho OCLP + Ivy Bridge |
| `Vault` | `'Secure'` | ✏️ **`'Optional'`** | Không dùng vault |

---

### NVRAM

| Đường dẫn | Default (Sample) | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `7C436110.../boot-args` | `'-v keepsyms=1'` | ✏️ **`'-v keepsyms=1 debug=0x100 npci=0x3000 alcid=1'`** | `npci=0x3000` BẮT BUỘC X79 |
| `7C436110.../csr-active-config` | `<00 00 00 00>` | ✏️ **`<03 00 00 00>`** | SIP partial (bit 0+1) cho OCLP patches |
| `7C436110.../prev-lang:kbd` | `ru-RU:252` (bytes) | ✏️ **`'en-US:0'`** (string) | Đặt ngôn ngữ bàn phím |
| `7C436110.../run-efi-updater` | `'No'` | ✅ Giữ | — |
| `LegacyEnable` | `False` | ✅ Giữ False | BIOS desktop có native NVRAM |
| `LegacyOverwrite` | `False` | ✅ Giữ False | — |
| `WriteFlash` | `True` | ✅ Giữ | — |

---

### PlatformInfo

| Đường dẫn | Default (Sample) | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `Generic/SystemProductName` | `'iMac19,1'` | ✏️ **`'MacPro6,1'`** | SMBIOS cho Ivy Bridge-EP Xeon |
| `Generic/SystemSerialNumber` | `'W00000000001'` | ✏️ **[GenSMBIOS output]** | Bắt buộc generate bằng GenSMBIOS |
| `Generic/MLB` | `'M0000000000000001'` | ✏️ **[GenSMBIOS output]** | Board Serial — bắt buộc generate |
| `Generic/SystemUUID` | `'00000000-...'` | ✏️ **[UUID mới]** | Generate random UUID |
| `Generic/ROM` | `<11 22 33 44 55 66>` | ✏️ **`<F4 5C 89 A5 50 8F>`** | WiFi MAC: `F4:5C:89:A5:50:8F` |
| `Generic/SpoofVendor` | `True` | ✅ Giữ | Apple Inc. vendor spoof |
| `UpdateDataHub` | `True` | ✅ Giữ | — |
| `UpdateNVRAM` | `True` | ✅ Giữ | — |
| `UpdateSMBIOS` | `True` | ✅ Giữ | — |
| `UpdateSMBIOSMode` | `'Create'` | ✅ Giữ | — |

---

### UEFI

#### UEFI/APFS

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `MinDate` | `0` | ✏️ **`-1`** | Cho phép mọi phiên bản APFS driver |
| `MinVersion` | `0` | ✏️ **`-1`** | Cho phép mọi phiên bản APFS |

#### UEFI/Drivers

| Driver | Action | Ghi chú |
|---|---|---|
| `OpenRuntime.efi` | ✏️ Giữ, `LoadEarly = True` | Bắt buộc |
| `HfsPlusLegacy.efi` | ➕ Thêm | Đọc HFS+ partition |
| `OpenCanopy.efi` | ➕ Thêm | GUI picker |
| 47 entries mẫu còn lại | 🗑️ Xoá hết | Không dùng |
| `OpenVariableRuntimeDxe.efi` | 🗑️ **Không dùng** | BIOS desktop có native NVRAM |

#### UEFI/Quirks

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `EnableVectorAcceleration` | `True` | ✅ Giữ | — |
| `IgnoreInvalidFlexRatio` | `False` | ✅ Giữ False | Chỉ Sandy Bridge mới cần `True` |
| `ReleaseUsbOwnership` | `False` | ✏️ **`True`** | EHCI handoff — USB hoạt động trước khi OS boot |
| `RequestBootVarRouting` | `True` | ✅ Giữ | Cần cho `LauncherOption=Full` |
| `ResizeGpuBars` | `-1` | ✅ Giữ | — |
| `TscSyncTimeout` | `0` | ✅ Giữ `0` | Dùng `CpuTscSync.kext` thay vì quirk này |
| `UnblockFsConnect` | `False` | ✅ Giữ | Không phải HP |

#### UEFI/Output

| Đường dẫn | Default | Giá trị cần đặt | Ghi chú |
|---|---|---|---|
| `ProvideConsoleGop` | `True` | ✅ Giữ | — |
| `Resolution` | `'Max'` | ✅ Giữ | Hoặc đặt `'1920x1080'` nếu muốn cố định |
| `TextRenderer` | `'BuiltinGraphics'` | ✅ Giữ | — |

---

### Tóm tắt số lượng thay đổi

| Section | Số field cần đổi | Mức độ |
|---|---|---|
| ACPI | Clear 3 lists + tuỳ SSDT | Đơn giản |
| Booter/Quirks | 3 field | Đơn giản |
| DeviceProperties | 1 field (layout-id đã đúng) | Không cần đổi |
| Kernel/Quirks | 5 field | Quan trọng |
| Kernel/Add | Clear + thêm 9-10 kexts | Quan trọng |
| Misc/Boot | 3 field | Đơn giản |
| Misc/Debug | 3 field | Tạm thời |
| Misc/Security | 4 field | **Quan trọng** |
| NVRAM/boot-args | 1 field | **Quan trọng** |
| PlatformInfo | 4 field (GenSMBIOS) | **Bắt buộc** |
| UEFI/APFS | 2 field | Đơn giản |
| UEFI/Drivers | Clear + thêm 3 driver | Đơn giản |
| UEFI/Quirks | 1 field | Đơn giản |

---

## Tham khảo

- [Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
- [OpenCore Legacy Patcher (OCLP)](https://github.com/dortania/OpenCore-Legacy-Patcher)
- `Guides/Tham_Khao_GitHub_X79.md` — tổng hợp repo X79 tham khảo
- [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) — tạo serial MacPro6,1
- [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X) — RealtekRTL8111.kext
- [acidanthera/CpuTscSync](https://github.com/acidanthera/CpuTscSync) — CpuTscSync.kext (thay thế VoodooTSCSync)
