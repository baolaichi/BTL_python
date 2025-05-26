from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder():
    # Tạo ảnh mới với nền trắng
    img = Image.new('RGB', (400, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ khung
    draw.rectangle([(0, 0), (399, 399)], outline='gray', width=2)
    
    # Vẽ biểu tượng hình ảnh
    draw.rectangle([(150, 150), (250, 250)], outline='gray', width=2)
    draw.line([(150, 200), (250, 200)], fill='gray', width=2)
    draw.line([(200, 150), (200, 250)], fill='gray', width=2)
    
    # Lưu ảnh
    img.save('placeholder.png')

if __name__ == '__main__':
    create_placeholder() 