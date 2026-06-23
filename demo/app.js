const canvas = document.getElementById('simulationCanvas');
const ctx = canvas.getContext('2d');

// DOM Elements
const popSlider = document.getElementById('popSlider');
const popValue = document.getElementById('popValue');
const supSlider = document.getElementById('supSlider');
const supValue = document.getElementById('supValue');
const speedSlider = document.getElementById('speedSlider');
const speedValue = document.getElementById('speedValue');
const modelRadios = document.getElementsByName('modelType');

const btnInit = document.getElementById('btnInit');
const btnStep = document.getElementById('btnStep');
const btnPlay = document.getElementById('btnPlay');
const btnPause = document.getElementById('btnPause');

const statTimestep = document.getElementById('statTimestep');
const statS = document.getElementById('statS');
const statI = document.getElementById('statI');
const statR = document.getElementById('statR');
const statPercolated = document.getElementById('statPercolated');

// Simulation Constants
const ENV_WIDTH = 10;
const INFECT_CUTOFF = 1;
const SUPER_INFECT = 1;
const INFECT_ALPHA = 2;
const RECOVER_PROB = 1;
const CANVAS_SIZE = 800;
const SCALE = CANVAS_SIZE / ENV_WIDTH;

// State
let population = [];
let timestep = 0;
let percolated = false;
let isPlaying = false;
let animationId = null;
let lastTime = 0;

class Individual {
    constructor(isPatientZero = false, superSpreaderProb) {
        this.healthState = "S";
        this.isSuperSpreader = Math.random() < superSpreaderProb;
        this.infectedBy = null;
        
        if (isPatientZero) {
            this.x = ENV_WIDTH / 2;
            this.y = 0;
            this.healthState = "I";
        } else {
            this.x = Math.random() * ENV_WIDTH;
            this.y = Math.random() * ENV_WIDTH;
        }
    }

    euclideanDistance(other) {
        let xDelta = Math.abs(this.x - other.x);
        if (xDelta > (ENV_WIDTH / 2)) {
            xDelta = ENV_WIDTH - xDelta;
        }
        let yDelta = Math.abs(this.y - other.y);
        return Math.sqrt(xDelta * xDelta + yDelta * yDelta);
    }

    infect(other, modelType) {
        let r = this.euclideanDistance(other);
        let prob = 0;

        if (modelType === 1) { // Strong
            if (r <= INFECT_CUTOFF) {
                if (this.isSuperSpreader) {
                    prob = SUPER_INFECT;
                } else {
                    prob = SUPER_INFECT * Math.pow(1 - r / INFECT_CUTOFF, INFECT_ALPHA);
                }
            }
        } else if (modelType === 2) { // Hub
            if (this.isSuperSpreader) {
                let r_n = INFECT_CUTOFF * Math.sqrt(6);
                if (r <= r_n) {
                    prob = SUPER_INFECT * Math.pow(1 - r / r_n, INFECT_ALPHA);
                }
            } else {
                if (r <= INFECT_CUTOFF) {
                    prob = SUPER_INFECT * Math.pow(1 - r / INFECT_CUTOFF, INFECT_ALPHA);
                }
            }
        }

        if (Math.random() < prob) {
            other.healthState = "I";
            other.infectedBy = this;
        }
    }

    recover() {
        if (Math.random() < RECOVER_PROB) {
            this.healthState = "R";
        }
    }
}

function initialize() {
    const envPop = parseInt(popSlider.value);
    const supProb = parseFloat(supSlider.value);
    
    population = [];
    population.push(new Individual(true, supProb)); // Patient Zero
    
    for (let i = 0; i < envPop - 1; i++) {
        population.push(new Individual(false, supProb));
    }
    
    timestep = 0;
    percolated = false;
    
    updateStats();
    draw();
    
    if (isPlaying) {
        pauseSimulation();
    }
}

function getModelType() {
    for (const radio of modelRadios) {
        if (radio.checked) {
            return parseInt(radio.value);
        }
    }
    return 1;
}

function step() {
    if (!population.some(ind => ind.healthState === "I")) {
        if (isPlaying) pauseSimulation();
        return;
    }

    let currentInfected = [];
    let currentSusceptible = [];
    
    for (let ind of population) {
        if (ind.healthState === "I") currentInfected.push(ind);
        else if (ind.healthState === "S") currentSusceptible.push(ind);
    }
    
    let modelType = getModelType();

    for (let ind_i of currentInfected) {
        for (let ind_s of currentSusceptible) {
            if (ind_s.healthState === "S") { // Might have been infected by another in this loop
                ind_i.infect(ind_s, modelType);
            }
        }
        ind_i.recover();
    }

    // Check percolation
    const envPop = parseInt(popSlider.value);
    const percolatesThreshold = ENV_WIDTH * (1 - 1 / Math.sqrt(envPop));
    
    let anyNewInfected = false;
    for (let ind of population) {
        if (ind.healthState === "I" && !currentInfected.includes(ind)) {
            anyNewInfected = true;
            if (ind.y >= percolatesThreshold) {
                percolated = true;
            }
        }
    }

    timestep++;
    updateStats();
    draw();
}

function updateStats() {
    let s = 0, i = 0, r = 0;
    for (let ind of population) {
        if (ind.healthState === "S") s++;
        else if (ind.healthState === "I") i++;
        else if (ind.healthState === "R") r++;
    }
    
    statTimestep.innerText = timestep;
    statS.innerText = s;
    statI.innerText = i;
    statR.innerText = r;
    
    statPercolated.innerText = percolated ? "Yes" : "No";
    statPercolated.className = "status-badge " + percolated;
}

function draw() {
    ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    
    // Draw connections first
    ctx.lineWidth = 1;
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    for (let ind of population) {
        if (ind.infectedBy) {
            let dx = Math.abs(ind.x - ind.infectedBy.x);
            if (dx <= ENV_WIDTH / 2) {
                ctx.beginPath();
                ctx.moveTo(ind.x * SCALE, ind.y * SCALE);
                ctx.lineTo(ind.infectedBy.x * SCALE, ind.infectedBy.y * SCALE);
                ctx.stroke();
            } else {
                // Wrapped line across cylinder edges
                let x1 = ind.x;
                let y1 = ind.y;
                let x2 = ind.infectedBy.x;
                let y2 = ind.infectedBy.y;
                
                if (x1 > x2) {
                    let tempX = x1; x1 = x2; x2 = tempX;
                    let tempY = y1; y1 = y2; y2 = tempY;
                }
                
                // x1 is near 0, x2 is near ENV_WIDTH
                // Draw segment going left from x1
                ctx.beginPath();
                ctx.moveTo(x1 * SCALE, y1 * SCALE);
                ctx.lineTo((x2 - ENV_WIDTH) * SCALE, y2 * SCALE);
                ctx.stroke();

                // Draw segment going right from x2
                ctx.beginPath();
                ctx.moveTo((x1 + ENV_WIDTH) * SCALE, y1 * SCALE);
                ctx.lineTo(x2 * SCALE, y2 * SCALE);
                ctx.stroke();
            }
        }
    }

    // Draw individuals
    for (let ind of population) {
        ctx.beginPath();
        ctx.arc(ind.x * SCALE, ind.y * SCALE, 4, 0, Math.PI * 2);
        
        if (ind.healthState === "S") {
            ctx.fillStyle = "#10b981"; // Emerald Green
        } else if (ind.healthState === "I") {
            ctx.fillStyle = "#f87171";
            // Pulse effect for infected
            ctx.shadowBlur = 10;
            ctx.shadowColor = "#f87171";
        } else {
            ctx.fillStyle = "#94a3b8";
        }
        
        ctx.fill();
        ctx.shadowBlur = 0; // reset

        // Draw superspreader ring
        if (ind.isSuperSpreader) {
            ctx.beginPath();
            ctx.arc(ind.x * SCALE, ind.y * SCALE, 6, 0, Math.PI * 2);
            ctx.strokeStyle = "#fbbf24";
            ctx.lineWidth = 1.5;
            ctx.stroke();
        }
    }
}

// Controls Logic
popSlider.addEventListener('input', (e) => { popValue.innerText = e.target.value; });
supSlider.addEventListener('input', (e) => { supValue.innerText = e.target.value; });
speedSlider.addEventListener('input', (e) => { 
    const val = parseInt(e.target.value);
    if(val > 70) speedValue.innerText = "Fast";
    else if(val > 30) speedValue.innerText = "Medium";
    else speedValue.innerText = "Slow";
});

btnInit.addEventListener('click', initialize);
btnStep.addEventListener('click', () => {
    if (isPlaying) pauseSimulation();
    step();
});

btnPlay.addEventListener('click', playSimulation);
btnPause.addEventListener('click', pauseSimulation);

function playSimulation() {
    isPlaying = true;
    btnPlay.style.display = 'none';
    btnPause.style.display = 'inline-block';
    
    function loop(timestamp) {
        if (!isPlaying) return;
        const speed = parseInt(speedSlider.value);
        const delay = 1010 - speed * 10; // Maps 1 to 1000ms, 100 to 10ms
        if (timestamp - lastTime >= delay) {
            step();
            lastTime = timestamp;
        }
        animationId = requestAnimationFrame(loop);
    }
    animationId = requestAnimationFrame(loop);
}

function pauseSimulation() {
    isPlaying = false;
    btnPlay.style.display = 'inline-block';
    btnPause.style.display = 'none';
    if (animationId) cancelAnimationFrame(animationId);
}

// Start
initialize();
