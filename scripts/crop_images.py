from PIL import Image
import os

uploads_dir = r'C:\Users\Felipe Oliveira\.gemini\antigravity\brain\531e9378-ee2e-4a98-b7dd-92a565062f27\.user_uploaded'
dest_dir = r'c:\Users\Felipe Oliveira\.octobrain\pc-tracker\web\public\images'
os.makedirs(dest_dir, exist_ok=True)

crops = {
    "cpu.jpg": ("media_1794488553303_dc71ab87.jpg", (100, 390, 440, 650)),
    "gpu.jpg": ("media_1794488553309_fd30e946.jpg", (140, 250, 500, 540)),
    "motherboard.jpg": ("media_1794488553286_b5c6306c.jpg", (140, 310, 500, 600)),
    "ram.jpg": ("media_1794488553305_57610424.jpg", (160, 240, 320, 550)),
    "ssd.jpg": ("media_1794488553292_d76ffa79.jpg", (50, 480, 550, 700)),
    "psu.jpg": ("media_1794488553288_88d9650a.jpg", (120, 370, 420, 650)),
    "cooler.jpg": ("media_1794488553283_100e19c1.jpg", (90, 480, 450, 710)),
}

for out_name, (src_file, box) in crops.items():
    p = os.path.join(uploads_dir, src_file)
    im = Image.open(p)
    cropped = im.crop(box)
    out_path = os.path.join(dest_dir, out_name)
    cropped.save(out_path, quality=95)
    print(f"SALVO: {out_name} - {cropped.size}")

# Para o monitor, vamos buscar uma imagem oficial limpa ou thumbnail
print("CROPS CONCLUÍDOS!")
