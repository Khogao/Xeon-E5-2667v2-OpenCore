# Tổng hợp GitHub Hackintosh tham khảo cho X79 + Xeon E5 v2

## Các repo quan trọng nhất

### ⭐ Ưu tiên cao — Cùng kiến trúc (X79 + Ivy Bridge-EP + AMD GPU)

| Repo | CPU | GPU | Mainboard | macOS | OC | Ghi chú |
|---|---|---|---|---|---|---|
| [nguyenphucdev/OpenCore_X79_X99_Xeon_E5_2650v2](https://github.com/nguyenphucdev/OpenCore_X79_X99_Xeon_E5_2650v2) | E5-2650 v2 | RX 470 | X79/X99 | Catalina | 0.6.1 | 🇻🇳 Người Việt, 19 stars — gần nhất với cấu hình này |
| [AwSomeSiz/Atermiter_X79G_Hackintosh](https://github.com/AwSomeSiz/Atermiter_X79G_Hackintosh) | E5-1650 v2 | RX 570 | Atermiter X79G | Big Sur→Ventura | 0.8.0 | Ivy Bridge-EP + AMD Polaris, ACPI đầy đủ, có Release |
| [antipeth/EFI-Motherboard-X79-OpenCore-Hackintosh](https://github.com/antipeth/EFI-Motherboard-X79-OpenCore-Hackintosh) | E5-2450 v2 | HD 7750 | **Huananzhi X79** | Monterey | 0.7.7 | Chính xác mainboard Huananzhi, chạy ổn |
| [mokk731/X79-E5v2-OpenCore-EFI](https://github.com/mokk731/X79-E5v2-OpenCore-EFI) | E5-2650 v2 | GTX 650 | X79-H67 | Catalina | 0.7.8 | Ghi chép rất chi tiết, nhiều bản EFI thử nghiệm, cập nhật 2025 |

### 📚 Tham khảo thêm

| Repo | Ghi chú |
|---|---|
| [cchs29/Hackintosh-huanan-X79-2650-k600-opencore-bigsur](https://github.com/cchs29/Hackintosh-huanan-X79-2650-k600-opencore-bigsur) | Huananzhi X79 + E5-2650, Big Sur |
| [xdien/hackintosh-x79-dual](https://github.com/xdien/hackintosh-x79-dual) | 🇻🇳 Dual Huananzhi X79 + E5-2620v2 (Clover, cũ) |
| [j1ans/X79-OpenCore-Catalina](https://github.com/j1ans/X79-OpenCore-Catalina) | Huanan X79, OpenCore, Catalina — 11 stars |
| [maklakowiktor/EFI-X79-HUANANZHI-ZD3-INTEL-XEON-E5-2640-V1-RX570-4GB](https://github.com/maklakowiktor/EFI-X79-HUANANZHI-ZD3-INTEL-XEON-E5-2640-V1-RX570-4GB) | Huananzhi ZD3 + RX570, Big Sur, hoạt động tốt |
| [verfasor/Hackintosh-X79-E5-2650-GTX-960](https://github.com/verfasor/Hackintosh-X79-E5-2650-GTX-960) | X79 + E5-2650, High Sierra (Clover) — 7 stars |

---

## ⚠️ Những điểm BẮT BUỘC cho X79 Ivy Bridge (KHÁC với X220)

### 1. `CpuTscSync.kext` — QUAN TRọNG NHẤT

> Thiếu kext này **chắc chắn bị treo** ở giai đoạn 2 boot (màn hình đen / panic).  
> Lý do: CPU X79 nhiều nhân không đồng bộ TSC giữa các core → macOS panic.

- Dùng **`CpuTscSync.kext`** (by acidanthera) — phiên bản hiện đại thay thế `VoodooTSCSync`
- Phị biến hơn VoodooTSCSync, hỗ trợ single và dual socket, cập nhật thường xuyên
- Link: [acidanthera/CpuTscSync](https://github.com/acidanthera/CpuTscSync) — v1.1.2

### 2. Boot-arg bắt buộc: `npci=0x3000`

```
boot-args: -v keepsyms=1 debug=0x100 npci=0x3000 alcid=1
```

Thiếu `npci=0x3000` sẽ không boot được trên X79 (PCI configuration issue).

### 3. Tắt "Above 4G Decoding" trong BIOS

Ngược với desktop Intel thế hệ mới — **phải TẮT** trên X79, nếu bật sẽ lỗi boot.

### 4. `SSDT-IMEI.aml` — Kiểm tra chipset

Cần thiết nếu mainboard dùng **6-series chipset** với Ivy Bridge CPU (ví dụ H67, P67, Z68).  
X79 dùng chipset Intel C600 — **thường không cần**, nhưng kiểm tra lại.

### 5. `AppleCpuPmCfgLock` + `AppleXcpmCfgLock` = YES

Hầu hết BIOS X79 Huananzhi không unlock CFG Lock được → cần bật cả hai quirk.

---

## ACPI Files cần thiết

| File | Mục đích | Ghi chú |
|---|---|---|
| `SSDT-PM.aml` | CPU Power Management | Tạo bằng `ssdtPRGen.sh` sau khi cài xong macOS |
| `SSDT-EC.aml` | Embedded Controller giả | Cần cho macOS Catalina+ |
| `SSDT-USBX.aml` | USB power injection | Cần cho USB 3.0 hoạt động đúng |
| `SSDT-RTC0-RANGE.aml` | Fix RTC | Một số bo X79 cần |
| `SSDT-IMEI.aml` | Intel MEI device | Chỉ cần nếu chipset 6-series |
| `DSDT.aml` (tuỳ chọn) | Override toàn bộ ACPI | Không khuyến nghị, dùng SSDT thay thế |

---

## Danh sách kext đầy đủ cho build này

### Bắt buộc

| Kext | Phiên bản | Mục đích |
|---|---|---|
| `Lilu.kext` | 1.7.1 | Patcher lõi — nạp trước tiên |
| `VirtualSMC.kext` | 1.3.7 | Giả lập SMC |
| `WhateverGreen.kext` | 1.7.0 | GPU / DRM patch |
| `AppleALC.kext` | 1.9.6 | Âm thanh onboard |
| `CpuTscSync.kext` | 1.1.2 | **Đồng bộ TSC — BẮT BUỘC cho X79** |

### Cảm biến & phần cứng

| Kext | Mục đích |
|---|---|
| `SMCProcessor.kext` | Nhiệt độ / công suất CPU |
| `SMCSuperIO.kext` | Quạt / cảm biến phần cứng |

### Mạng

| Kext | Mục đích | Trạng thái |
|---|---|---|
| `RealtekRTL8111.kext` | **Realtek RTL8168/8111** (`VEN_10EC&DEV_8168`) — đã xác nhận WMI | ✅ Cần tải |

> ⚠️ **Đã xác nhận**: Mainboard dùng **Realtek RTL8168** (`VEN_10EC&DEV_8168`), KHÔNG phải Intel.  
> **KHÔNG dùng** `IntelMausi.kext` — máy này không có Intel NIC.  
> Tải từ: [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X)

### WiFi & Bluetooth — Native (không cần kext)

> 🎉 **Phát hiện quan trọng**: Card WiFi là **Broadcom BCM43602 Apple OEM**!

| Thiết bị | DeviceID | Hỗ trợ macOS |
|---|---|---|
| WiFi: BCM43602 | `PCI\VEN_14E4&DEV_43BA&SUBSYS_0133106B&REV_01` | ✅ Native — KHÔNG cần kext |
| BT: Apple Broadcom | `USB\VID_05AC&PID_8290` | ✅ Native — KHÔNG cần kext |

**Subsystem `106B` = Apple vendor ID** → đây là card Apple OEM dùng trong MacBook Pro và iMac.  
Hỗ trợ đầy đủ: AirDrop, Handoff, Continuity, AirPlay Receiver, iMessage, FaceTime native.

> ✅ **Không cần** AirportItlwm, itlwm, AirportBrcmFixup, BrcmPatchRAM, hay bất kỳ WiFi/BT kext nào.

---

## Mẹo từ các repo trên

### Bị treo ở giai đoạn 2

```
virtualsmc cần thêm boot-arg: vsmcgen=1
```

### Lỗi "OC: Grabbed zero system-id for SB"

```
Misc -> Security -> SecureBootModel -> Disabled
```

### Lỗi "Panic diags file unavailable"

```
Thay đổi thứ tự kext: VirtualSMC → SMCSuperIO → SMCProcessor
```

### Cài đặt xong nhưng reboot không vào macOS

```
Misc -> Security -> SecureBootModel -> Disabled
```

### Không nhận USB 3.0

```
Dùng USBToolBox chạy từ Windows để map USB trước khi cài macOS.
Không cần và không nên bật XhciPortLimit (broken từ macOS 11.3+).
https://github.com/USBToolBox/tool
```

---

## Thứ tự unlock CFG Lock trên X79 BIOS

> Nguồn: [mokk731/X79-E5v2-OpenCore-EFI — 解锁CFG Lock.md](https://github.com/mokk731/X79-E5v2-OpenCore-EFI/blob/main/解锁CFG%20Lock.md)

Nếu BIOS không có tuỳ chọn CFG Lock:
1. Dùng `ControlMsrE2.efi` tool trong OpenCore Tools để unlock qua shell
2. Hoặc chỉ cần để `AppleCpuPmCfgLock = YES` và `AppleXcpmCfgLock = YES` là đủ

---

## So sánh nhanh với máy của bạn

| Thông số | Các repo tham khảo | Máy của bạn | Đánh giá |
|---|---|---|---|
| CPU | E5-2650 v2 / E5-1650 v2 | **E5-2667 v2** | ✅ Cùng kiến trúc Ivy Bridge-EP |
| GPU | RX 470 / RX 570 | **RX 580 (DEV_67DF)** | ✅ Cùng Polaris, driver giống hệt |
| Mainboard | Huananzhi / Atermiter X79 | **HUANANZHI X79 V2.49PB** (đã xác nhận) | ✅ Cùng chipset C600/C200 |
| RAM | DDR3 ECC 1333/1600 | **48GB Samsung DDR3 1333 ECC** | ✅ Tương thích |
| Audio | Realtek ALC897/ALC662 | **Realtek ALC887** (`DEV_0887`) | ✅ AppleALC hỗ trợ, layout-id: 1 |
| Ethernet | Realtek RTL8111 | **Realtek RTL8168** (`DEV_8168`) | ✅ RealtekRTL8111.kext |
| WiFi | Card rời / Intel / không có | **BCM43602 Apple OEM** | 🎉 Tốt hơn — native macOS! |
| Bluetooth | Không có / USB dongle | **Apple Broadcom native** | 🎉 Tốt hơn — native macOS! |
| USB 3.0 | VIA / Etron / Renesas | **VIA VL805** | ✅ Hỗ trợ, cần USB map |
| macOS đã thử | Catalina / Big Sur / Ventura | mục tiêu: **Sequoia 15.x** | ✅ Đã xác nhận hoạt động (Reddit 2026) |
| Boot Drive | Bất kỳ SSD | **Apple SSD SM0128G 128GB SATA** | ✅ Native, không cần NVMeFix |

---

## Kết luận cho build này

> Build **Xeon E5-2667 v2 + Huananzhi X79 + RX 580** có cấu hình phần cứng **thuận lợi hơn** hầu hết các repo tham khảo vì:
> 1. **WiFi BCM43602** — native macOS, không cần kext, full AirDrop/Handoff
> 2. **RX 580** — AMD Polaris native, không cần WEG GPU patch đặc biệt
> 3. **Apple SSD SM0128G** — SATA SSD native, không cần NVMeFix
> 4. **48GB ECC RAM** — macOS nhận đủ, ổn định hơn non-ECC
>
> Điểm cần chú ý: **VoodooTSCSync.kext** (bắt buộc X79) và **npci=0x3000** (bắt buộc X79).
