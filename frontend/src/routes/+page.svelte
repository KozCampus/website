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


    });

    

    
</script>


<!-- Navigation -->
<nav class="navbar" id="navbar">
    <div class="nav-container">
        <a href="#hero" class="logo">KözCampus</a>
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
                    <div class="feature-icon">📱</div>
                    <h3 class="feature-title">Jog és politika</h3>
                    <p class="feature-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                <div class="feature-card fade-in-element">
                    <div class="feature-icon">⚡</div>
                    <h3 class="feature-title">Agrárium</h3>
                    <p class="feature-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                <div class="feature-card fade-in-element">
                    <div class="feature-icon">👥</div>
                    <h3 class="feature-title">Művészetek</h3>
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
                <h3 class="footer-title">KözCampus</h3>
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
                    <a href="/" class="social-link" aria-label="Facebook">f</a>
                    <a href="/" class="social-link" aria-label="Twitter">𝕏</a>
                    <a href="/" class="social-link" aria-label="LinkedIn">in</a>
                    <a href="/" class="social-link" aria-label="Instagram">📷</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 KözCampus. Minden jog fenntartva.</p>
        </div>
    </div>
</footer>




<svelte:window bind:scrollY={y} />