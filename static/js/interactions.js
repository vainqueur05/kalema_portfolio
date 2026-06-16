// ====== CURSEUR CUSTOM – Jony Ive + Elon Musk ======
const cursor = document.getElementById('custom-cursor');
if (cursor) {
    let mouseX = 0, mouseY = 0, cursorX = 0, cursorY = 0;
    document.addEventListener('mousemove', (e) => { mouseX = e.clientX; mouseY = e.clientY; });
    function animateCursor() {
        cursorX += (mouseX - cursorX) * 0.2;
        cursorY += (mouseY - cursorY) * 0.2;
        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';
        requestAnimationFrame(animateCursor);
    }
    animateCursor();
    document.addEventListener('mousedown', () => cursor.style.transform = 'translate(-50%, -50%) scale(0.7)');
    document.addEventListener('mouseup', () => cursor.style.transform = 'translate(-50%, -50%) scale(1)');
    // Agrandissement au survol des éléments interactifs
    document.querySelectorAll('a, button, .project-btn, .reaction-btn, .filter-btn, .quiz-option, .curiosity-point').forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });
}

// ====== TYPOGRAPHIE CINÉTIQUE – Steve Jobs ======
function animateWords(selector) {
    document.querySelectorAll(selector).forEach(el => {
        const text = el.innerText.trim();
        el.innerHTML = '';
        text.split(' ').forEach((word, i) => {
            const span = document.createElement('span');
            span.className = 'word';
            span.style.transitionDelay = i * 0.04 + 's';
            span.textContent = word + ' ';
            el.appendChild(span);
        });
    });
}
document.addEventListener('DOMContentLoaded', () => {
    animateWords('h2.kinetic-title, h1.kinetic-title');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) entry.target.querySelectorAll('.word').forEach(w => w.classList.add('visible')); });
    }, { threshold: 0.4 });
    document.querySelectorAll('.kinetic-title').forEach(el => observer.observe(el));
});

// ====== RÉACTIONS – Mark Zuckerberg ======
function loadReactions() {
    document.querySelectorAll('.reactions').forEach(container => {
        const card = container.closest('.card-project');
        if (!card) return;
        const slug = card.getAttribute('data-slug');
        if (!slug) return;
        const saved = JSON.parse(localStorage.getItem(`reactions_${slug}`) || '{}');
        container.querySelectorAll('.reaction-btn').forEach(btn => {
            const icon = btn.querySelector('i');
            let type = '';
            if (icon.classList.contains('fa-fire')) type = 'fire';
            else if (icon.classList.contains('fa-heart')) type = 'heart';
            else if (icon.classList.contains('fa-rocket')) type = 'rocket';
            const countSpan = btn.querySelector('.reaction-count');
            if (countSpan && saved[type]) countSpan.textContent = saved[type];
        });
    });
}
function saveReaction(slug, type, count) {
    const saved = JSON.parse(localStorage.getItem(`reactions_${slug}`) || '{}');
    saved[type] = count;
    localStorage.setItem(`reactions_${slug}`, JSON.stringify(saved));
}
function spawnConfetti() {
    for (let i = 0; i < 20; i++) {
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';
        piece.style.left = Math.random() * 100 + 'vw';
        piece.style.backgroundColor = ['#E50914','#ff4d4d','#ffd700','#00ff88','#ff6b6b'][Math.floor(Math.random()*5)];
        piece.style.animationDuration = (Math.random() * 1 + 0.5) + 's';
        document.body.appendChild(piece);
        setTimeout(() => piece.remove(), 1500);
    }
}
document.addEventListener('click', (e) => {
    const btn = e.target.closest('.reaction-btn');
    if (!btn) return;
    const icon = btn.querySelector('i');
    if (!icon) return;
    let type = '';
    if (icon.classList.contains('fa-fire')) type = 'fire';
    else if (icon.classList.contains('fa-heart')) type = 'heart';
    else if (icon.classList.contains('fa-rocket')) type = 'rocket';
    if (!type) return;
    const countSpan = btn.querySelector('.reaction-count');
    const card = btn.closest('.card-project');
    if (!card) return;
    const slug = card.getAttribute('data-slug');
    if (!slug || !countSpan) return;
    let count = parseInt(countSpan.textContent) || 0;
    count++;
    countSpan.textContent = count;
    saveReaction(slug, type, count);
    btn.style.transform = 'scale(1.4)';
    setTimeout(() => btn.style.transform = '', 200);
    spawnConfetti();
});
document.addEventListener('DOMContentLoaded', loadReactions);

// ====== MENU MOBILE – Don Norman ======
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.querySelectorAll('a, button').forEach(el => {
            el.addEventListener('click', () => mobileMenu.classList.add('hidden'));
        });
    }
});

// ====== EXIT INTENT – Cialdini (réciprocité + rareté) ======
let exitPopupShown = false;
let exitTimer;
document.addEventListener('mouseleave', (e) => {
    if (!exitPopupShown && e.clientY <= 0) {
        clearTimeout(exitTimer);
        exitTimer = setTimeout(() => {
            const popup = document.getElementById('exit-popup');
            if (popup) { popup.classList.add('active'); exitPopupShown = true; }
        }, 600);
    }
});
document.addEventListener('mouseenter', () => clearTimeout(exitTimer));
document.addEventListener('click', (e) => { if (e.target.id === 'close-exit-popup') document.getElementById('exit-popup')?.classList.remove('active'); });

// ====== SCROLL PROGRESS – Elon Musk ======
document.addEventListener('DOMContentLoaded', () => {
    const bar = document.createElement('div');
    bar.id = 'global-progress';
    bar.style.cssText = 'position:fixed; top:0; left:0; height:3px; background:linear-gradient(90deg, #E50914, #ff4d4d); z-index:9999; width:0%; transition: width 0.15s linear; border-radius: 0 2px 2px 0;';
    document.body.appendChild(bar);
    window.addEventListener('scroll', () => {
        bar.style.width = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight) * 100) + '%';
    });
});

// ====== LAZY LOADING – Jeff Bezos ======
document.addEventListener('DOMContentLoaded', () => {
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) img.src = img.dataset.src;
                img.onload = () => img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    lazyImages.forEach(img => observer.observe(img));
});

// ====== COMPTEURS ANIMÉS – Warren Buffett ======
function animateCounters() {
    document.querySelectorAll('.stat-number:not(.counted)').forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const suffix = counter.getAttribute('data-suffix') || '';
        const duration = 2500;
        let start = null;
        const step = (timestamp) => {
            if (!start) start = timestamp;
            const progress = Math.min((timestamp - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            counter.textContent = Math.floor(eased * target) + suffix;
            if (progress < 1) requestAnimationFrame(step);
            else counter.classList.add('counted');
        };
        requestAnimationFrame(step);
    });
}
document.addEventListener('DOMContentLoaded', () => {
    const section = document.getElementById('impact');
    if (section) {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) animateCounters();
        else {
            const obs = new IntersectionObserver((entries) => {
                entries.forEach(entry => { if (entry.isIntersecting) { animateCounters(); obs.unobserve(entry.target); } });
            }, { threshold: 0.3 });
            obs.observe(section);
        }
    }
});

// ====== SALUTATION + GÉOLOC – Arnaud Montebourg ======
document.addEventListener('DOMContentLoaded', () => {
    const hour = new Date().getHours();
    const el = document.getElementById('greeting');
    if (el) el.textContent = (hour >= 18 || hour < 5 ? 'Bonsoir' : hour >= 14 ? 'Bon après-midi' : 'Bonjour') + ', je suis';
    fetch('https://ipapi.co/json/').then(r => r.json()).then(data => {
        const loc = document.getElementById('location');
        if (loc) loc.innerHTML = `<i class="fas fa-map-marker-alt text-netflix-accent"></i> ${data.city}, ${data.country_name}`;
    }).catch(() => {
        const loc = document.getElementById('location');
        if (loc) loc.textContent = '📍 Quelque part dans le monde';
    });
});

// ====== PHRASE D'ACCROCHE – Jack Ma ======
document.addEventListener('DOMContentLoaded', () => {
    const taglines = [
        "Je ne code pas des applis. Je construis des ponts invisibles.",
        "Transformer le réel en numérique, sans friction.",
        "Votre vision, ma stack technique.",
        "L'Afrique innove, je code cette innovation.",
        "Chaque ligne de code est un pas vers votre succès."
    ];
    const el = document.getElementById('dynamic-tagline');
    if (el) { let i = 0; setInterval(() => { el.style.opacity = '0'; setTimeout(() => { el.textContent = taglines[i % taglines.length]; el.style.opacity = '1'; }, 300); i++; }, 5000); }
});

// ====== FILTRES PROJETS – Dan Lok ======
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('bg-netflix-accent', 'text-white'));
        btn.classList.add('bg-netflix-accent', 'text-white');
        const filter = btn.dataset.filter;
        document.querySelectorAll('.swiper-slide').forEach(slide => {
            slide.style.display = (filter === 'all' || slide.dataset.category === filter) ? '' : 'none';
        });
        if (typeof swiper !== 'undefined') swiper.update();
    });
});

// ====== MODES ZEN/LECTURE – Neil Rackham ======
document.addEventListener('DOMContentLoaded', () => {
    const zen = document.getElementById('zen-mode');
    const lecture = document.getElementById('lecture-mode');
    if (zen && lecture) {
        zen.addEventListener('click', () => {
            document.body.classList.toggle('zen'); zen.classList.toggle('active');
            if (document.body.classList.contains('reading')) { document.body.classList.remove('reading'); lecture.classList.remove('active'); }
        });
        lecture.addEventListener('click', () => {
            document.body.classList.toggle('reading'); lecture.classList.toggle('active');
            if (document.body.classList.contains('zen')) { document.body.classList.remove('zen'); zen.classList.remove('active'); }
        });
    }
});

// ====== KONAMI CODE – Elon Musk ======
let konami = [];
const secret = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'];
window.addEventListener('keydown', (e) => {
    konami.push(e.key); if (konami.length > secret.length) konami.shift();
    if (JSON.stringify(konami) === JSON.stringify(secret)) {
        const overlay = document.getElementById('konami-overlay');
        if (overlay) overlay.classList.remove('hidden');
    }
});

// ====== EASTER EGG – Bill Gates ======
window.addEventListener('orientationchange', () => {
    if (window.orientation === 90 || window.orientation === -90) {
        const toast = document.createElement('div');
        toast.style.cssText = 'position:fixed; bottom:20px; left:50%; transform:translateX(-50%); background:#E50914; color:white; padding:12px 24px; border-radius:30px; z-index:9999; animation: fadeIn 0.3s;';
        toast.textContent = '🐣 Easter egg : Bridge Afrika, le code au service de l\'impact.';
        document.body.appendChild(toast);
        setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3000);
    }
});
// ====== CANVAS PARTICULES (Hero) ======
const heroCanvas = document.getElementById('hero-particles');
if (heroCanvas) {
    const ctx = heroCanvas.getContext('2d');
    let width = heroCanvas.width = heroCanvas.parentElement.offsetWidth;
    let height = heroCanvas.height = heroCanvas.parentElement.offsetHeight;
    const particles = [];
    const particleCount = 80;

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.3;
            this.speedY = (Math.random() - 0.5) * 0.3;
            this.opacity = Math.random() * 0.3 + 0.05;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x < 0 || this.x > width) this.speedX *= -1;
            if (this.y < 0 || this.y > height) this.speedY *= -1;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(229, 9, 20, ' + this.opacity + ')';
            ctx.fill();
        }
    }

    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function animateParticles() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(function(p) {
            p.update();
            p.draw();
        });
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 120) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = 'rgba(229, 9, 20, ' + (0.08 * (1 - distance / 120)) + ')';
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animateParticles);
    }
    animateParticles();

    window.addEventListener('resize', function() {
        width = heroCanvas.width = heroCanvas.parentElement.offsetWidth;
        height = heroCanvas.height = heroCanvas.parentElement.offsetHeight;
    });
}
// ====== BADGE DISPONIBILITÉ – Cialdini ======
document.addEventListener('DOMContentLoaded', () => {
    const badge = document.querySelector('.fixed.bottom-4.left-4');
    if (badge) {
        let places = 2;
        setInterval(() => {
            const span = badge.querySelector('span:not(.w-2)');
            if (span) {
                places = Math.max(1, places === 2 ? 2 : 1);
                span.textContent = places > 1 ? `${places} créneaux disponibles ce mois` : 'Dernier créneau disponible';
            }
        }, 45000);
    }
});
// ====== LOUPE PROCESS ======
const zones = document.querySelectorAll('.frise-zone');
const loupeText = document.getElementById('loupe-text');
zones.forEach(zone => {
    zone.addEventListener('mouseenter', () => {
        loupeText.textContent = zone.getAttribute('data-detail');
    });
    zone.addEventListener('mouseleave', () => {
        loupeText.textContent = 'Survolez une zone pour voir le détail.';
    });
});

// ====== COMPTEUR DE TEMPS ======
const slider = document.getElementById('time-slider');
const timeDisplay = document.getElementById('time-display');
const anecdote = document.getElementById('time-anecdote');
const anecdotes = {
    50: "50h : optimisation SEO → +20% de trafic organique.",
    120: "120h : dashboard e‑commerce → lancement anticipé d'une semaine.",
    200: "200h : automatisation des rapports → fini les tâches manuelles.",
    350: "350h : migration cloud → zéro interruption.",
    500: "500h : refonte complète → nouveau business model."
};
slider.addEventListener('input', () => {
    const val = slider.value;
    timeDisplay.textContent = val + ' heures';
    // Trouver l'anecdote la plus proche
    const keys = Object.keys(anecdotes).map(Number).sort((a,b)=>a-b);
    let bestKey = keys[0];
    for (let k of keys) {
        if (val >= k) bestKey = k;
    }
    anecdote.textContent = anecdotes[bestKey] || '';
});

// ====== CARTE À GRATTER ======
document.querySelectorAll('.scratch-card').forEach(card => {
    card.addEventListener('click', function() {
        if (this.classList.contains('revealed')) return;
        this.classList.add('revealed');
        this.innerHTML = '<i class="fas fa-lightbulb text-2xl mb-2"></i><p class="text-white text-sm">' + this.getAttribute('data-message') + '</p>';
        // petit son ?
    });
});

// ====== SYNTHÉ SONORE (simulation) ======
const skillBtns = document.querySelectorAll('.skill-btn');
const syntheMessage = document.getElementById('synthe-message');
skillBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        btn.classList.toggle('active');
        // Son simulé via AudioContext (optionnel)
        const activeSkills = document.querySelectorAll('.skill-btn.active');
        const names = Array.from(activeSkills).map(b => b.textContent.trim());
        if (names.length > 0) {
            syntheMessage.textContent = names.join(' + ') + ' = Votre projet unique.';
        } else {
            syntheMessage.textContent = 'Chaque techno est un son – ensemble, elles font votre projet.';
        }
    });
});

// ====== PUZZLE PROBLÈME → SOLUTION ======
document.querySelectorAll('.puzzle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const caseType = btn.getAttribute('data-case');
        const solutions = {
            lent: "Optimisation des images, mise en cache, CDN → temps de chargement divisé par 4.",
            panier: "Rappel par email/SMS + tunnel de paiement simplifié → +25% de conversion.",
            mobile: "PWA ou app native légère, adaptée au réseau local → vos clients vous ont dans la poche."
        };
        document.getElementById('puzzle-result').textContent = solutions[caseType] || '';
    });
});

// ====== CARTE DU MONDE (simulée) ======
const worldCanvas = document.getElementById('worldMap');
if (worldCanvas) {
    const wctx = worldCanvas.getContext('2d');
    wctx.fillStyle = '#E50914';
    wctx.fillRect(50, 50, 5, 5);
    wctx.font = '12px Inter';
    wctx.fillStyle = '#B3B3B3';
    wctx.fillText('🌍 Afrique • Europe • Amériques', 20, 100);
}
// ====== RADAR ======
const radarCanvas = document.getElementById('radar-canvas');
if (radarCanvas) {
    const ctx = radarCanvas.getContext('2d');
    let angle = 0;
    function drawRadar() {
        ctx.clearRect(0, 0, 300, 300);
        ctx.strokeStyle = 'rgba(229,9,20,0.3)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(150, 150, 100, 0, Math.PI * 2);
        ctx.stroke();
        // Ligne de balayage
        ctx.strokeStyle = '#E50914';
        ctx.beginPath();
        ctx.moveTo(150, 150);
        const x = 150 + 100 * Math.cos(angle);
        const y = 150 + 100 * Math.sin(angle);
        ctx.lineTo(x, y);
        ctx.stroke();
        angle += 0.02;
        requestAnimationFrame(drawRadar);
    }
    drawRadar();

    // Offres sur les blips
    const blips = document.querySelectorAll('.radar-blip');
    const offerText = document.getElementById('radar-offer');
    blips.forEach(blip => {
        blip.addEventListener('click', () => {
            offerText.textContent = 'Offre : ' + blip.getAttribute('data-offer');
        });
    });
}

// ====== JEU DU DÉTAIL ======
let detailScore = 0;
document.querySelectorAll('.detail-guess').forEach(btn => {
    btn.addEventListener('click', () => {
        const answer = btn.getAttribute('data-answer');
        const result = document.getElementById('detail-result');
        if (answer === 'cache') {
            result.textContent = 'Correct ! La mise en cache a réduit le temps de 80%.';
            btn.classList.add('correct');
        } else {
            result.textContent = 'Raté ! La bonne réponse était : mise en cache.';
            btn.classList.add('wrong');
        }
        // Désactiver tous les boutons
        document.querySelectorAll('.detail-guess').forEach(b => b.disabled = true);
    });
});
// ====== PARI INVERSÉ ======
(function() {
    const radioOptions = document.querySelectorAll('input[name="challenge"]');
    const selectedDisplay = document.getElementById('selectedOptionDisplay');
    const challengeFormContainer = document.getElementById('challengeFormContainer');
    const triggerBtn = document.getElementById('triggerChallengeBtn');
    const challengeForm = document.getElementById('challengeForm');

    const optionLabels = {
        'opt-speed': 'Optimisation vitesse : gagner 0.5s de chargement',
        'opt-auto': 'Automatisation d\'une tâche manuelle',
        'opt-conversion': 'Audit conversion en 15 min'
    };

    function updateDisplayedOption() {
        let selectedValue = null;
        for (let radio of radioOptions) {
            if (radio.checked) {
                selectedValue = radio.value;
                break;
            }
        }
        if (selectedValue && optionLabels[selectedValue]) {
            selectedDisplay.value = optionLabels[selectedValue];
        } else {
            selectedDisplay.value = optionLabels['opt-speed'];
        }
    }

    updateDisplayedOption();
    for (let radio of radioOptions) {
        radio.addEventListener('change', updateDisplayedOption);
    }

    triggerBtn.addEventListener('click', function() {
        if (challengeFormContainer.classList.contains('hidden')) {
            challengeFormContainer.classList.remove('hidden');
            challengeFormContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            challengeFormContainer.classList.add('hidden');
        }
    });

    challengeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = challengeForm.querySelector('input[type="email"]').value.trim();
        const project = challengeForm.querySelector('input[type="text"]:not(#selectedOptionDisplay)').value.trim();
        const challengeDesc = selectedDisplay.value;
        
        if (!email || !project) {
            alert("Veuillez remplir l'email et le nom du projet.");
            return;
        }
        // Envoyer à l'API (à créer plus tard) ou afficher une confirmation
        alert(`Défi reçu !\n\nEmail : ${email}\nProjet : ${project}\nDéfi : ${challengeDesc}\n\nJe vous réponds sous 48h max.`);
        
        challengeForm.reset();
        challengeFormContainer.classList.add('hidden');
        const counterSpan = document.getElementById('challengesCounter');
        let currentCount = parseInt(counterSpan.innerText);
        if (!isNaN(currentCount)) {
            counterSpan.innerText = currentCount + 1;
        } else {
            counterSpan.innerText = '48';
        }
        // Déclencher confetti
        spawnConfetti();
    });

    // Horloge
    let totalSeconds = 48 * 3600;
    const clockElement = document.getElementById('trustClock');
    
    function updateClockDisplay() {
        if (totalSeconds < 0) totalSeconds = 48 * 3600;
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        clockElement.innerText = `${hours.toString().padStart(2,'0')}h${minutes.toString().padStart(2,'0')}m`;
        if (totalSeconds > 0) totalSeconds--;
    }
    updateClockDisplay();
    setInterval(updateClockDisplay, 60000);
})();
// ====== EFFETS COGNITIFS PHOTO SILHOUETTE ======
const photo = document.getElementById('profile-photo');
const photoContainer = document.getElementById('photo-container');
const monaEyes = document.querySelectorAll('.mona-eye');

if (photo && photoContainer) {
    // 1. ŒIL DE DIEU + MONA LISA
    document.addEventListener('mousemove', function(e) {
        if (!monaEyes.length) return;
        const rect = photoContainer.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 3;
        const deltaX = (e.clientX - centerX) / 25;
        const deltaY = (e.clientY - centerY) / 25;
        monaEyes.forEach(function(eye) {
            eye.style.transform = 'translate(' + deltaX + 'px, ' + deltaY + 'px)';
        });
    });

    // 2. RÉTENTION D'ATTENTION
    let inactivityTimer;
    function resetInactivity() {
        clearTimeout(inactivityTimer);
        photo.classList.remove('growing');
        inactivityTimer = setTimeout(function() {
            photo.classList.add('growing');
        }, 5000);
    }
    document.addEventListener('mousemove', resetInactivity);
    document.addEventListener('scroll', resetInactivity);
    resetInactivity();

    // 3. PHOTO SYMBIOTIQUE
    window.addEventListener('scroll', function() {
        const scrollY = window.scrollY;
        const maxScroll = 500;
        const scale = Math.min(1 + (scrollY / maxScroll) * 0.15, 1.15);
        photo.style.transform = 'scale(' + scale + ')';
    });

    // 4. EFFET DÉJÀ-VU
    const variants = ['variant-1', 'variant-2', 'variant-3'];
    const randomVariant = variants[Math.floor(Math.random() * variants.length)];
    photo.classList.add(randomVariant);
}