<script lang="ts">
    import { onMount } from 'svelte';

    let isMobileMenuOpen = false;
    let y: number; // Scroll Position

    let hero: any;
    let hitvallas: any;
    let szervezet: any;
    let events: any;
    let layer1: any;
    let layer2: any;

    function toggleMobileMenu() {
        isMobileMenuOpen = !isMobileMenuOpen;
        if (isMobileMenuOpen) {
            document.documentElement.classList.add('scrollBlock');
            document.body.classList.add('scrollBlock');
        } else {
            document.documentElement.classList.remove('scrollBlock');
            document.body.classList.remove('scrollBlock');
        }
    }

    function hideMobileMenu() {
        isMobileMenuOpen = false;
        document.documentElement.classList.remove('scrollBlock');
        document.body.classList.remove('scrollBlock');
    }

    function isInside(name: any) {
        if (name == undefined) return false;
        return (y >= name.offsetTop && y < name.offsetTop + name.offsetHeight)
    }

    onMount(() => {
        const fadeElements = document.querySelectorAll('.fade-in-element');

        const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, index * 100);
                fadeInObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        fadeElements.forEach(element => {
            fadeInObserver.observe(element);
        });

        // Preloader
        const STAGGER = 300;
        const BASE_DURATION = 800;
        const preloader = document.getElementById('preloader');
        const svg = document.getElementById('logo-svg') as SVGElement | null;
        const paths = svg?.querySelectorAll('.anim-path') || [];

        if (svg) {
            svg.style.setProperty('--path-duration', `${BASE_DURATION}ms`);
        }

        paths.forEach((p, i) => {
            setTimeout(() => p.classList.add('visible'), i * STAGGER);
        });

        const total = BASE_DURATION + STAGGER * (paths.length - 1) + 800;
        if (preloader) {
            setTimeout(() => {
                preloader.classList.add('hidden');
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 600);
            }, total);
        }
    });

    

    
</script>




<div class="preloader" id="preloader">
    <div class="logo-wrap">
        <svg id="logo-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4959.32 3284.43" width="260" height="260">
            <defs>
                <style>
                    .cls-1{fill:#18242d;}.cls-2{opacity:0.6;}.cls-3{fill:#327d4e;}.cls-4{fill:#17232d;}.cls-5{fill:#327e4e;}.cls-6{fill:#fadb3e;}.cls-7{fill:#83b094;}.cls-8{fill:#fcea8a;}
                </style>
            </defs>
            <g class="cls-2" transform="matrix(1.924374, 0, 0, 1.924374, -4971.255859, -2912.801025)">
                <path class="cls-5 anim-path" d="M3912.05,1976.71c-83.44-43.59-151.15-94.65-244.84-85.46s-180.32,71.51-218.85,157.4c-46.37,103.36-24.76,228.58-76.28,329.48-17.46,34.19-42.55,63.84-62.64,96.56-65.52,106.74-71.21,251.78-1,355.5S3527,2981.77,3639,2925.74c128.36-64.22,180.22-233,311.33-291.41,82.53-36.78,177.8-21.18,267.57-31.38,97.71-11.1,194.89-41,251-121.81s62.79-197.61,2.33-275.16c-70.08-89.87-196.84-124.9-309.21-143.9C4098.81,2051.39,4045.36,2046.36,3912.05,1976.71Z"/>
            </g>
            <g class="cls-2" transform="matrix(1.924374, 0, 0, 1.924374, -4971.255859, -2912.801025)">
                <path class="cls-6 anim-path" d="M4195.38,1911.54c1.27-60.89-73.22-281.36-309.84-164.89-119.61,58.87-62.5,225.13-174.85,318.65-73.79,61.42-124.39,56.84-287.84,71.19-84.57,7.43-228.64,74.28-255.78,278.42-27.48,206.68,259.64,416.33,475.84,254.82,316.83-236.68,257.3,350.73,560.35,106.87,196.75-158.31-56.46-385.91-87.93-439.48-88.87-151.29-27.62-224.6,12-272.45C4147.42,2040.45,4194,1977.91,4195.38,1911.54Z"/>
            </g>
            <path class="cls-4 anim-path" d="M 1865.69 2070.97 C 2156.52 2242.95 2506.01 2348.76 2824.8 2236.76 C 3143.59 2124.76 3392.49 1817.24 3406.33 1479.61 C 3410.02 1389.82 3397.84 1298.51 3362.58 1215.86 C 3289.59 1044.68 3113.65 922.903 2927.83 913.103 C 2755.33 904.003 2590.78 982.983 2443.37 1072.99 C 2295.96 1163.01 2153.87 1267.35 1988.97 1318.77 C 1890.65 1349.43 1784.46 1361.11 1696.46 1414.68 C 1625.86 1457.6 1560.39 1523.74 1546.05 1605.1 C 1503.22 1848.25 1769.91 2014.34 1865.69 2070.97 Z"/>
      </svg>
    </div>
</div>

<!-- Navigation -->
<nav class="navbar" id="navbar">
    <div class="nav-container">
        <a href="#hero" class="logo"><img src="/11_fullface.svg" alt="KözCampus"></a>
        <button class="hamburger" class:active={isMobileMenuOpen} onclick={toggleMobileMenu} aria-label="Toggle menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <ul class="nav-links" id="navLinks" class:active={isMobileMenuOpen}>
            <li><a href="#hero" class="nav-link" class:active={isInside(hero) || isInside(layer1) || isInside(layer2)} onclick={hideMobileMenu}>Kezdőlap</a></li>
            <li><a href="#hitvallas" class="nav-link" class:active={isInside(hitvallas)} onclick={hideMobileMenu}>Hitvallás</a></li>
            <li><a href="#szervezet" class="nav-link" class:active={isInside(szervezet)} onclick={hideMobileMenu}>Szervezetünk</a></li>
            <li><a href="#events" class="nav-link" class:active={isInside(events)} onclick={hideMobileMenu}>Események</a></li>
        </ul>
    </div>
</nav>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<main onclick={hideMobileMenu} onkeydown={()=>{}}>
    <!-- Hero Section -->
    <section class="hero" id="hero" bind:this={hero}>
        <div class="hero-content">
            <h1 class="hero-title animate-fade-in">A szabad gondolatok közössége</h1>
            <p class="hero-subtitle animate-fade-in">Lorem ipsum dolor sit amet, consectetur adipiscing elit. In eros leo, cursus et iaculis aliquet, posuere eget diam.</p>
            <div class="hero-buttons animate-fade-in">
                <a href="/" class="btn btn-primary">Jelentkezz!</a>
                <a href="#hitvallas" class="btn btn-secondary">Tudj meg többet!</a>
            </div>
        </div>
    </section>

    <div class="spacer layer2" bind:this={layer1}></div>
    <div class="spacer layer1" bind:this={layer2}></div>

    <!-- Hitvallás Section -->
    <section class="about" id="hitvallas" bind:this={hitvallas}>
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Hitvallásunk</h2>
                <p class="section-subtitle">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </div>
            <div class="features-grid">
                <div class="feature-card fade-in-element">
                    <div class="feature-icon"><i class="fa-solid fa-gavel jog"></i></div>
                    <h3 class="feature-title jog">Jog és politika</h3>
                    <p class="feature-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                <div class="feature-card fade-in-element">
                    <div class="feature-icon"><i class="fa-solid fa-wheat-awn agrar"></i></div>
                    <h3 class="feature-title agrar">Agrárium</h3>
                    <p class="feature-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                <div class="feature-card fade-in-element">
                    <div class="feature-icon"><i class="fa-solid fa-masks-theater muveszet"></i></div>
                    <h3 class="feature-title muveszet">Művészetek</h3>
                    <p class="feature-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Szervezet Section -->
    <section class="services" id="szervezet" bind:this={szervezet}>
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Szervezetünk</h2>
                <p class="section-subtitle">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </div>
            <div class="bento-grid">
                <div class="bento-item bento-large fade-in-element">
                    <div class="bento-content">
                        <h3>Elnökség</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                    </div>
                </div>
                <div class="bento-item fade-in-element">
                    <div class="bento-content">
                        <h3>Tematikus felelősök</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                    </div>
                </div>
                <div class="bento-item fade-in-element">
                    <div class="bento-content">
                        <h3>Jogi csapat</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                    </div>
                </div>
                <div class="bento-item bento-tall fade-in-element">
                    <div class="bento-content">
                        <h3>Facilitátorok</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                    </div>
                </div>
                <div class="bento-item fade-in-element">
                    <div class="bento-content">
                        <h3>Háttérmunka</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                    </div>
                </div>
                <div class="bento-item fade-in-element">
                    <div class="bento-content">
                        <h3>Eseményszervezés</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Események Section -->
    <section class="testimonials" id="events" bind:this={events}>
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Események</h2>
                <p class="section-subtitle">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </div>
            <div class="testimonials-grid">
                <div class="testimonial-card fade-in-element">
                    <p class="testimonial-quote">"Lorem ipsum dolor sit amet, consectetur adipiscing elit. In eros leo, cursus et iaculis aliquet, posuere eget diam."</p>
                    <div class="testimonial-author">
                        <div class="avatar">XY</div>
                        <div class="author-info">
                            <div class="author-name">Dzama-Demjén Péter</div>
                            <div class="author-position">International Businessman</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card fade-in-element">
                    <p class="testimonial-quote">"Lorem ipsum dolor sit amet, consectetur adipiscing elit. In eros leo, cursus et iaculis aliquet, posuere eget diam."</p>
                    <div class="testimonial-author">
                        <div class="avatar">XY</div>
                        <div class="author-info">
                            <div class="author-name">Dzama-Demjén Péter</div>
                            <div class="author-position">International Businessman</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card fade-in-element">
                    <p class="testimonial-quote">"Lorem ipsum dolor sit amet, consectetur adipiscing elit. In eros leo, cursus et iaculis aliquet, posuere eget diam."</p>
                    <div class="testimonial-author">
                        <div class="avatar">XY</div>
                        <div class="author-info">
                            <div class="author-name">Dzama-Demjén Péter</div>
                            <div class="author-position">International Businessman</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</main>

<!-- Footer -->
<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-column">
                <img src="/11_fullface.svg" alt="KözCampus" class="footer-logo">
                <p class="footer-text">A szabad gondolatok közössége</p>
            </div>
            <div class="footer-column">
                <h4 class="footer-heading">Gyors elérés</h4>
                <ul class="footer-links">
                    <li><a href="#hero">Kezdőlap</a></li>
                    <li><a href="#hitvallas">Hitvallás</a></li>
                    <li><a href="#szervezet">Szervezet</a></li>
                    <li><a href="#events">Események</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h4 class="footer-heading">Kapcsolatfelvétel</h4>
                <div class="social-links">
                    <a href="/" class="social-link" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
                    <a href="/" class="social-link" aria-label="Twitter"><i class="fa-brands fa-x-twitter"></i></a>
                    <a href="/" class="social-link" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
                    <a href="/" class="social-link" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 KözCampus. Minden jog fenntartva.</p>
        </div>
    </div>
</footer>




<svelte:window bind:scrollY={y} />