import os
import sys
import subprocess
from pathlib import Path

# Imageio orqali yuklangan ffmpeg manzilini tizim PATH ga majburiy ulaymiz
try:
    import imageio_ffmpeg
    ffmpeg_bin = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    if ffmpeg_bin not in os.environ["PATH"]:
        os.environ["PATH"] += os.path.pathsep + ffmpeg_bin
except ImportError:
    pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_audio_file():
    print("="*60)
    print("      AI POWERED VOCAL REMOVER & INSTRUMENTAL EXTRACTOR      ")
    print("="*60)
    
    current_dir = Path.cwd()
    
    while True:
        print(f"\n📂 Joriy ishchi papka: {current_dir}")
        file_input = input("🎵 Fayl nomini kiriting (masalan: Nalalar):\n👉 ").strip()
        
        file_input = file_input.replace('"', '').replace("'", "")
        file_path = Path(file_input)
        
        possible_names = [
            file_input, 
            f"{file_input}.mp3", 
            f"{file_input}.wav",
            f"{file_input}.mp3.mp3"
        ]
        
        if not file_path.is_file():
            for name in possible_names:
                check_path = current_dir / name
                if check_path.is_file():
                    file_path = check_path
                    break

        if file_path.is_file():
            print(f"\n✅ Fayl muvaffaqiyatli topildi: {file_path.name}")
            return file_path
        else:
            print("❌ Xato: Fayl topilmadi! Fayl ushbu loyiha papkasida ekanligini tekshiring.")

def extract_instrumental(file_path):
    output_dir = file_path.parent / "Output_Minus"
    output_dir.mkdir(exist_ok=True)
    
    print("\n[+] Sun'iy intellekt ishga tushmoqda...")
    print("[+] Demucs backend ishlamoqda. Iltimos kuting, bu biroz vaqt oladi...\n")
    
    # MUHIM: torchaudio xatolarini aylanib o'tish uchun demucs ichki qismini Python buyrug'i sifatida chaqiramiz
    # --jobs 1 protsessor yukini normallashtiradi, --two-stems faqat vokal va minus ajratadi
    command = [
        sys.executable, "-m", "demucs.separate",
        "--two-stems", "vocals",
        "-n", "htdemucs",
        "-o", str(output_dir),
        str(file_path)
    ]
    
    try:
        # Kod Python ichidan turib Demucs'ni tizim darajasida majburlab yurgizadi
        subprocess.run(command, check=True)
        
        track_name = file_path.stem
        result_folder = output_dir / "htdemucs" / file_path.stem
        
        instrumental_source = result_folder / "no_vocals.wav"
        vocal_source = result_folder / "vocals.wav"
        
        final_instrumental = output_dir / f"{track_name} [Minus].wav"
        final_vocal = output_dir / f"{track_name} [Vocal].wav"
        
        if instrumental_source.exists():
            if final_instrumental.exists(): os.remove(final_instrumental)
            instrumental_source.rename(final_instrumental)
        if vocal_source.exists():
            if final_vocal.exists(): os.remove(final_vocal)
            vocal_source.rename(final_vocal)
            
        if result_folder.exists(): os.rmdir(result_folder)
        if (output_dir / "htdemucs").exists(): os.rmdir(output_dir / "htdemucs")
            
        clear_screen()
        print("="*60)
        print("🎉 MUKAMMAL MINUS TAYYOR BO'LDI!")
        print("="*60)
        print(f"\n📂 Natijalar: {output_dir}")
        print(f"🎵 Minus (Instrumental): {final_instrumental.name}")
        print(f"🎤 Faqat Vokal: {final_vocal.name}\n")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Demucs rendersiz to'xtadi. Xato kodi: {e}")
    except Exception as ex:
        print(f"\n❌ Kutilmagan texnik xatolik: {ex}")

if __name__ == "__main__":
    clear_screen()
    audio_file = get_audio_file()
    extract_instrumental(audio_file)