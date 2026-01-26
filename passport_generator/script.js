const ELEMENTS = {
    dropZone: document.getElementById('dropZone'),
    imageInput: document.getElementById('imageInput'),
    outputCanvas: document.getElementById('outputCanvas'),
    downloadBtn: document.getElementById('downloadBtn'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    placeholderOverlay: document.getElementById('placeholderOverlay'),
    statusIndicator: document.getElementById('statusIndicator'),
    previewCard: document.getElementById('previewCard')
};

const CONSTANTS = {
    PHOTO_WIDTH: 35, // mm
    PHOTO_HEIGHT: 45, // mm
    DPI: 300,
    MM_PER_INCH: 25.4,
    BORDER_WIDTH: 2, // mm
    A4_WIDTH: 210, // mm
    A4_HEIGHT: 297 // mm
};

let originalImage = null;

// Initialization
function init() {
    setupEventListeners();
}

function setupEventListeners() {
    // File Input
    ELEMENTS.imageInput.addEventListener('change', handleFileSelect);

    // Drag & Drop
    ELEMENTS.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        ELEMENTS.dropZone.classList.add('dragover');
    });

    ELEMENTS.dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        ELEMENTS.dropZone.classList.remove('dragover');
    });

    ELEMENTS.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        ELEMENTS.dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // Download
    ELEMENTS.downloadBtn.addEventListener('click', downloadPhotos);
}

function handleFileSelect(e) {
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
}

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Per favore carica un file immagine valido (JPG, PNG).');
        return;
    }

    setLoadingState(true);

    const reader = new FileReader();
    reader.onload = function(e) {
        originalImage = new Image();
        originalImage.onload = function() {
            // Artificial delay for "processing" feel
            setTimeout(() => {
                generatePhotoSheet();
                setLoadingState(false);
                setStatus('Pronto', true);
            }, 1500);
        }
        originalImage.src = e.target.result;
    }
    reader.readAsDataURL(file);
}

function generatePhotoSheet() {
    const ctx = ELEMENTS.outputCanvas.getContext('2d');
    
    // Calculate pixels based on DPI
    const pixelsPerMM = CONSTANTS.DPI / CONSTANTS.MM_PER_INCH;
    const photoWidthPx = Math.round(CONSTANTS.PHOTO_WIDTH * pixelsPerMM);
    const photoHeightPx = Math.round(CONSTANTS.PHOTO_HEIGHT * pixelsPerMM);
    const borderWidthPx = Math.round(CONSTANTS.BORDER_WIDTH * pixelsPerMM);
    
    // Set Canvas Dimensions (High Res for Print)
    ELEMENTS.outputCanvas.width = Math.round(CONSTANTS.A4_WIDTH * pixelsPerMM);
    ELEMENTS.outputCanvas.height = Math.round(CONSTANTS.A4_HEIGHT * pixelsPerMM);
    
    // White Background
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, ELEMENTS.outputCanvas.width, ELEMENTS.outputCanvas.height);
    
    // Grid Calculation
    const photosPerRow = Math.floor(CONSTANTS.A4_WIDTH / (CONSTANTS.PHOTO_WIDTH + CONSTANTS.BORDER_WIDTH));
    const photosPerColumn = Math.floor(CONSTANTS.A4_HEIGHT / (CONSTANTS.PHOTO_HEIGHT + CONSTANTS.BORDER_WIDTH));
    
    const totalWidthUsed = (photosPerRow * (CONSTANTS.PHOTO_WIDTH + CONSTANTS.BORDER_WIDTH)) - CONSTANTS.BORDER_WIDTH;
    const totalHeightUsed = (photosPerColumn * (CONSTANTS.PHOTO_HEIGHT + CONSTANTS.BORDER_WIDTH)) - CONSTANTS.BORDER_WIDTH;
    
    // Centering Logic
    const marginMmLeft = (CONSTANTS.A4_WIDTH - totalWidthUsed) / 2;
    const marginMmTop = (CONSTANTS.A4_HEIGHT - totalHeightUsed) / 2;
    
    const startX = Math.round(marginMmLeft * pixelsPerMM);
    const startY = Math.round(marginMmTop * pixelsPerMM);
    
    // Draw Photos
    for(let row = 0; row < photosPerColumn; row++) {
        for(let col = 0; col < photosPerRow; col++) {
            const x = startX + col * (photoWidthPx + borderWidthPx);
            const y = startY + row * (photoHeightPx + borderWidthPx);
            
            // Draw Photo
            // In a real app, face detection logic would go here to crop centering the face.
            // Here we just scale the image to fit 'cover' style logic
            drawImageCover(ctx, originalImage, x, y, photoWidthPx, photoHeightPx);
            
            // Draw Cut Guide (Light Gray Border)
            ctx.strokeStyle = '#e5e7eb';
            ctx.lineWidth = 1; // 1px for guide is enough
            ctx.strokeRect(x, y, photoWidthPx, photoHeightPx);
        }
    }
    
    // Hide placeholder
    ELEMENTS.placeholderOverlay.style.display = 'none';
    
    // Enable button
    ELEMENTS.downloadBtn.disabled = false;
    ELEMENTS.dropZone.style.borderColor = '#10b981';
    ELEMENTS.dropZone.style.background = 'rgba(16, 185, 129, 0.05)';
    
    // Animate Preview Reveal
    ELEMENTS.outputCanvas.style.animation = 'none';
    ELEMENTS.outputCanvas.offsetHeight; /* trigger reflow */
    ELEMENTS.outputCanvas.style.animation = 'fadeInUp 0.5s ease-out';
}

/**
 * Helper to draw image covering the area (like object-fit: cover)
 */
function drawImageCover(ctx, img, x, y, w, h) {
    const imgRatio = img.width / img.height;
    const targetRatio = w / h;
    
    let sx, sy, sWidth, sHeight;
    
    if (imgRatio > targetRatio) {
        // Image is wider than target
        sHeight = img.height;
        sWidth = img.height * targetRatio;
        sy = 0;
        sx = (img.width - sWidth) / 2;
    } else {
        // Image is taller than target
        sWidth = img.width;
        sHeight = img.width / targetRatio;
        sx = 0;
        sy = (img.height - sHeight) / 2;
    }
    
    ctx.drawImage(img, sx, sy, sWidth, sHeight, x, y, w, h);
}

function setLoadingState(isLoading) {
    if (isLoading) {
        ELEMENTS.loadingOverlay.classList.add('active');
        ELEMENTS.downloadBtn.disabled = true;
        setStatus('Elaborazione...', false);
    } else {
        ELEMENTS.loadingOverlay.classList.remove('active');
    }
}

function setStatus(text, isReady) {
    ELEMENTS.statusIndicator.innerHTML = `
        <span class="dot"></span> ${text}
    `;
    if (isReady) {
        ELEMENTS.statusIndicator.classList.add('ready');
    } else {
        ELEMENTS.statusIndicator.classList.remove('ready');
    }
}

function downloadPhotos() {
    const link = document.createElement('a');
    link.download = 'fototessere_A4.png';
    link.href = ELEMENTS.outputCanvas.toDataURL('image/png', 1.0);
    link.click();
}

// Start
init();
