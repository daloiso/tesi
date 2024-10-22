// Inizializza variabili globali
let audioContext;
let mediaRecorder;
let audioChunks = [];

// Funzione per iniziare la registrazione
async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const input = audioContext.createMediaStreamSource(stream);
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        
        // Salva la traccia registrata sul server
        const formData = new FormData();
        formData.append('recording', audioBlob, 'recording.mp3');
        
        // Invia la registrazione al server se necessario (da implementare)
        // await fetch('/save_recording', { method: 'POST', body: formData });
    };

    mediaRecorder.start();
}

// Funzione per fermare la registrazione
function stopRecording() {
    mediaRecorder.stop();
    audioChunks = [];
}

// Funzione per riprodurre la musica
function playMusic(musicFile) {
    const audio = new Audio(`static/music/${musicFile}`);
    audio.play();
}

// Funzione per gestire il submit del form
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene l'invio del form

    const musicFile = document.getElementById('music_file').value;
    const userText = document.getElementByI
}