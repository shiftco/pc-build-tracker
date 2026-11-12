from PIL import Image, ImageDraw, ImageFilter
import os

dest_dir = r'c:\Users\Felipe Oliveira\.octobrain\pc-tracker\web\public\images'
keys = ['cpu', 'gpu', 'motherboard', 'ram', 'ssd', 'psu', 'cooler', 'monitor']
target_bg = (24, 24, 27) # Exato #18181b (Tailwind bg-zinc-900)

for k in keys:
    p = os.path.join(dest_dir, f'{k}.jpg')
    im = Image.open(p).convert('RGB')
    w, h = im.size
    
    # Criamos uma máscara para floodfill a partir das bordas
    # Usamos imagem temporária para marcar o fundo com uma cor única (magenta puro)
    temp = im.copy()
    seed_points = [
        (0, 0), (w-1, 0), (0, h-1), (w-1, h-1),
        (w//2, 0), (w//2, h-1), (0, h//2), (w-1, h//2)
    ]
    
    # No cooler, existem dois vãos internos entre as mangueiras com fundo branco
    if k == 'cooler':
        # Procura pixels brancos puros (r>248, g>248, b>248) na região das mangueiras (x > 340, y > 280)
        for sx in range(350, 560, 10):
            for sy in range(280, 480, 10):
                r, g, b = temp.getpixel((sx, sy))
                if r > 248 and g > 248 and b > 248:
                    seed_points.append((sx, sy))

    for pt in seed_points:
        try:
            r, g, b = temp.getpixel(pt)
            if r > 230 and g > 230 and b > 230:
                ImageDraw.floodfill(temp, pt, (255, 0, 255), thresh=38)
        except:
            pass

    # Cria máscara binária onde temp == (255, 0, 255)
    mask = Image.new('L', (w, h), 0)
    temp_px = temp.load()
    mask_px = mask.load()
    for y in range(h):
        for x in range(w):
            if temp_px[x, y] == (255, 0, 255):
                mask_px[x, y] = 255

    # Suaviza levemente a máscara para anti-aliasing perfeito nas bordas
    mask_smooth = mask.filter(ImageFilter.GaussianBlur(radius=0.8))

    # Compõe a imagem original sobre o fundo escuro #18181b (bg-zinc-900)
    dark_canvas = Image.new('RGB', (w, h), target_bg)
    final_im = Image.composite(dark_canvas, im, mask_smooth)
    final_im.save(p, 'JPEG', quality=95)
    print(f"Processado dark mode #18181b: {k}.jpg")

# Gera grid final para conferência visual
grid_dark = Image.new('RGB', (4 * 220, 2 * 220), (9, 9, 11))
for idx, k in enumerate(keys):
    im_s = Image.open(os.path.join(dest_dir, f'{k}.jpg')).resize((200, 200), Image.Resampling.LANCZOS)
    x = (idx % 4) * 220 + 10
    y = (idx // 4) * 220 + 10
    grid_dark.paste(im_s, (x, y))

grid_dark.save(r'C:\Users\Felipe Oliveira\.gemini\antigravity\brain\531e9378-ee2e-4a98-b7dd-92a565062f27\scratch_grid_final.jpg', quality=95)
print("GRID FINAL SALVO!")
