import os
import sys
import subprocess
from pathlib import Path

# Imageio orqali yuklangan ffmpeg manzilini tizim PATH ga ulaymiz
try:
    import imageio_ffmpeg
    ffmpeg_bin = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    if ffmpeg_bin not in os.environ["PATH"]:
        os.environ["PATH"] += os.path.pathsep + ffmpeg_bin
except ImportError:
    pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def convert_wav_to_mp3():
    clear_screen()
    print("="*60)
    print("         💎 WAV TO MP3 (320kbps) HIGH-QUALITY CONVERTER        ")
    print("="*60)
    
    # Joriy ishchi papka va Output_Minus manzili
    current_dir = Path.cwd()
    output_dir = current_dir / "Output_Minus"
    
    if not output_dir.exists():
        print(f"❌ Xato: '{output_dir.name}' papkasi topilmadi! Avval vokalni ajratib oling.")
        return

    # Papka ichidagi hamma .wav fayllarni qidirib topamiz
    wav_files = list(output_dir.glob("*.wav"))
    
    if not wav_files:
        print("ℹ️ Papka ichida o'zgartirish uchun .wav fayllar topilmadi.")
        return

    print(f"\n📂 Topilgan fayllar soni: {len(wav_files)} ta")
    print("[+] MP3 formatiga o'tkazish (conversion) boshlanmoqda...\n")

    for wav_file in wav_files:
        # Yangi hosil bo'ladigan MP3 faylning to'liq manzili
        mp3_file = wav_file.with_suffix(".mp3")
        
        print(f"⏳ O'zgartirilmoqda: {wav_file.name}  ➡️  {mp3_file.name}")
        
        # FFmpeg buyrug'i: -ab 320k (audio bitrate 320 kbps - eng yuqori sifat)
        command = [
            "ffmpeg",
            "-i", str(wav_file),
            "-ab", "320k",
            "-y",  # Agar eski MP3 mavjud bo'lsa, ustidan yozib yuborish
            str(mp3_file)
        ]
        
        try:
            # FFmpeg'ni orqa fonda yurgizish (shovqinsiz ishlashi uchun stdout/stderr yopiladi)
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"✅ Muvaffaqiyatli bajarildi!")
            
            # 🔥 SIZGA LAYFHAK: Joy tejash uchun original .wav faylini o'chirib tashlashni xohlasangiz,
            # pastdagi qator boshidagi '#' belgisini olib tashlang:
            # os.remove(wav_file)
            
        except subprocess.CalledProcessError:
            print(f"❌ Xatolik: {wav_file.name} faylini o'tkazib bo'lmadi.")
        except Exception as e:
            print(f"❌ Kutilmagan xato: {e}")

    print("\n" + "="*60)
    print("🎉 BARCHA AUDIO FAYLLAR 320KBPS MP3 GA AYLANTIRILDI!")
    print("="*60)
    print(f"📂 Fayllar shu papkada saqlandi: {output_dir}\n")

if __name__ == "__main__":
    convert_wav_to_mp3()