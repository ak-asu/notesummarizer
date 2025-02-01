import subprocess
import tqdm


class CustomProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n  
        
    def update(self, n):
        super().update(n)
        self._current += n
        
        print("Audio Transcribe Progress: " + str(round(self._current/self.total*100))+ "%")

def get_device():
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "cuda" if result.returncode == 0 else "cpu"
    except FileNotFoundError:
        return "cpu"