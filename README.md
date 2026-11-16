# ⚡ QR-Max

> **Advanced URL QR Code Generator & Terminal Renderer**  
> *Zero-install CLI utility featuring live terminal previews, custom color themes, smooth gradients, and optional center logo embedding.*

---

## 🚀 Features

* **Zero-Install Core:** Built using Python's standard library (`urllib`), requiring no heavy package setup for basic usage.
* **Terminal ASCII Preview:** Instantly renders live ANSI QR codes directly in your console.
* **Solid & Gradient Themes:** Choose from multiple luxury and cyber color palettes, including solid variants and smooth multi-color horizontal gradients.
* **Optional Center Logo:** Seamlessly embed custom branding from `/home/kali/` with automatic scaling and aspect-ratio preservation.
* **Direct-to-Downloads:** Automatically saves output directly to your system's `~/Downloads/` directory with clean terminal feedback.

---

## 🎨 Color & Gradient Themes

| Option | Theme Name | Type | Description |
| :---: | :--- | :---: | :--- |
| **1** | **Classic Black** | Solid | Standard high-contrast black-on-white QR modules. |
| **2** | **Matrix Green** | Solid | Hacker-inspired terminal green aesthetic. |
| **3** | **Cyber Blue** | Solid | Sleek futuristic neon blue. |
| **4** | **Neon Red** | Solid | High-visibility warning red. |
| **5** | **Metallic Gold** | Solid | Luxury dark-and-gold aesthetic (`#FFD700`). |
| **6** | **Blue & Red Gradient** | Gradient | Smooth horizontal transition from electric blue to neon red. |
| **7** | **Purple & Pink Gradient** | Gradient | Vibrant violet-to-magenta hue shift. |
| **8** | **Cyan & Purple Gradient** | Gradient | Deep cyberpunk aqua-to-purple transition. |
| **9** | **Sunset Orange & Gold** | Gradient | Warm, high-end radiant gradient blend. |

---

## 📦 Requirements & Dependencies

* **Python 3.x** (Standard library used for networking and generation)
* **Pillow (`PIL`)** *(Optional)*: Required only if you want to use gradients or embed a center logo. Install via:
  ```bash
  pip install Pillow
