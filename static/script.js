document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const loader = document.querySelector('.loader');
    const transcriptElement = document.getElementById('transcript');
    const summaryElement = document.getElementById('summary');
    
    // Clear previous results
    transcriptElement.textContent = '';
    summaryElement.textContent = '';

    let formData = new FormData();
    formData.append('file', document.getElementById('file-input').files[0]);

    // Show loader
    loader.classList.remove('hidden');

    fetch('/transcribe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide loader
        loader.classList.add('hidden');
        
        if (data.transcript) {
            transcriptElement.textContent = data.transcript;
        }
        if (data.summary) {
            // Remove asterisks and set summary text
            summaryElement.textContent = data.summary.replace(/\*\*/g, '');
        }
    })
    .catch(error => {
        // Hide loader
        loader.classList.add('hidden');
        console.error('Error:', error);
    });
});

document.getElementById('generate-pdf').addEventListener('click', function() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Add Title
    doc.setFontSize(22);
    doc.text("Audio Transcription and Summarization", 10, 10);

    // Add Transcription
    doc.setFontSize(16);
    doc.text("Transcription:", 10, 30);
    doc.setFontSize(12);
    const transcriptionText = document.getElementById('transcript').textContent || 'No transcription available.';
    doc.text(transcriptionText, 10, 40);

    // Add Summary
    doc.setFontSize(16);
    doc.text("Summary:", 10, 60);
    doc.setFontSize(12);
    const summaryText = document.getElementById('summary').textContent || 'No summary available.';
    doc.text(summaryText, 10, 70);

    // Save the PDF
    doc.save("transcription_summary.pdf");
});

document.getElementById('generate-doc').addEventListener('click', function() {
    const transcriptionText = document.getElementById('transcript').textContent || 'No transcription available.';
    const summaryText = document.getElementById('summary').textContent || 'No summary available.';
    
    const content = `
        <h1>Audio Transcription and Summarization</h1>
        <h2>Transcription:</h2>
        <p>${transcriptionText}</p>
        <h2>Summary:</h2>
        <p>${summaryText}</p>
    `;

    const blob = new Blob([content], {
        type: 'application/msword'
    });

    saveAs(blob, 'transcription_summary.doc');
});


