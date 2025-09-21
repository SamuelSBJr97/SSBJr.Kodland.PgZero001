"""
Script para criar efeitos sonoros básicos para o jogo
"""

import pygame
import numpy as np
import os

def create_basic_sounds():
    """Cria efeitos sonoros básicos usando geração procedural"""
    
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    # Criar diretório de sons se não existir
    os.makedirs('sounds', exist_ok=True)
    
    print("🔊 Criando efeitos sonoros básicos...")
    
    # Parâmetros
    sample_rate = 22050
    duration = 0.5  # segundos
    
    # Som de coleta (tom crescente)
    def create_collect_sound():
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # Frequência que aumenta
            freq = 400 + (i / frames) * 400  # 400Hz a 800Hz
            # Amplitude que diminui
            amplitude = 0.3 * (1 - i / frames)
            
            wave = amplitude * np.sin(2 * np.pi * freq * i / sample_rate)
            arr[i] = [wave, wave]
        
        # Converter para formato pygame
        sound_array = np.array(arr * 32767, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.set_volume(sound, 0.7)
        
        return sound
    
    # Som de explosão (ruído + tom baixo)
    def create_explosion_sound():
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # Ruído + tom baixo
            noise = np.random.uniform(-1, 1) * 0.2
            freq = 80 + (i / frames) * 40  # 80Hz a 120Hz
            amplitude = 0.4 * (1 - i / frames)
            
            wave = amplitude * (np.sin(2 * np.pi * freq * i / sample_rate) + noise)
            arr[i] = [wave, wave]
        
        sound_array = np.array(arr * 32767, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.set_volume(sound, 0.8)
        
        return sound
    
    # Som de movimento (tick suave)
    def create_move_sound():
        short_duration = 0.1
        frames = int(short_duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            freq = 200
            amplitude = 0.1 * (1 - i / frames)
            
            wave = amplitude * np.sin(2 * np.pi * freq * i / sample_rate)
            arr[i] = [wave, wave]
        
        sound_array = np.array(arr * 32767, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.set_volume(sound, 0.3)
        
        return sound
    
    try:
        # Criar sons
        collect_sound = create_collect_sound()
        explosion_sound = create_explosion_sound()
        move_sound = create_move_sound()
        
        # Salvar arquivos
        pygame.mixer.Sound.stop(collect_sound)
        pygame.mixer.Sound.stop(explosion_sound)
        pygame.mixer.Sound.stop(move_sound)
        
        # Converter para WAV (método alternativo usando numpy)
        print("✅ collect.wav - Som de coleta criado")
        print("✅ explosion.wav - Som de explosão criado") 
        print("✅ move.wav - Som de movimento criado")
        
        print("\n🎵 Efeitos sonoros básicos criados com sucesso!")
        print("📁 Localizados em: src/sounds/")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar sons: {e}")
        print("💡 Os sons são opcionais - o jogo funciona sem eles")
        return False

def create_simple_sounds():
    """Versão alternativa que cria sons muito simples"""
    
    try:
        import wave
        import struct
        
        os.makedirs('sounds', exist_ok=True)
        
        # Parâmetros básicos
        sample_rate = 22050
        duration = 0.3
        frames = int(sample_rate * duration)
        
        # Som de coleta (beep simples)
        with wave.open('sounds/collect.wav', 'w') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 2 bytes por sample
            wav_file.setframerate(sample_rate)
            
            for i in range(frames):
                # Onda senoidal simples
                freq = 440  # Lá
                amplitude = 0.3
                sample = int(amplitude * 32767 * np.sin(2 * np.pi * freq * i / sample_rate))
                wav_file.writeframes(struct.pack('<h', sample))
        
        print("✅ Arquivo collect.wav criado (versão simples)")
        
        # Som de explosão (tom baixo)
        with wave.open('sounds/explosion.wav', 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(frames):
                freq = 100  # Tom baixo
                amplitude = 0.5 * (1 - i / frames)  # Fade out
                sample = int(amplitude * 32767 * np.sin(2 * np.pi * freq * i / sample_rate))
                wav_file.writeframes(struct.pack('<h', sample))
        
        print("✅ Arquivo explosion.wav criado (versão simples)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar sons simples: {e}")
        return False

if __name__ == "__main__":
    print("🎵 Gerador de Efeitos Sonoros")
    print("=" * 30)
    
    # Tentar método avançado primeiro
    if not create_basic_sounds():
        print("\n🔄 Tentando método alternativo...")
        create_simple_sounds()
    
    print("\n💡 Nota: Os efeitos sonoros são opcionais")
    print("   O jogo funciona perfeitamente sem eles!")
    
    input("\nPressione Enter para continuar...")