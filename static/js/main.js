document.addEventListener('DOMContentLoaded', function() {
  // ─── Loading Screen ────────────────────────────────────────────────────────
  const loader = document.getElementById('loading-screen');
  if (loader) {
    window.addEventListener('load', function() {
      setTimeout(() => {
        loader.classList.add('hidden');
      }, 500); // Small delay for visual impact
    });
    // Fallback if load event already fired or delayed
    setTimeout(() => {
      loader.classList.add('hidden');
    }, 2500);
  }

  // ─── Navbar Scroll Effect ──────────────────────────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
    });
  }

  // ─── Hero Slider ───────────────────────────────────────────────────────────
  const slides = document.querySelectorAll('.hero-slide');
  if (slides.length > 1) {
    let currentSlide = 0;
    slides[0].classList.add('active');
    
    setInterval(() => {
      slides[currentSlide].classList.remove('active');
      currentSlide = (currentSlide + 1) % slides.length;
      slides[currentSlide].classList.add('active');
    }, 4500);
  }

  // ─── Animated Counters ─────────────────────────────────────────────────────
  const counters = document.querySelectorAll('.counter');
  if (counters.length > 0) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = entry.target;
          const targetValue = parseInt(target.getAttribute('data-target'));
          const suffix = target.getAttribute('data-suffix') || '';
          let startValue = 0;
          const duration = 1500; // 1.5s
          const stepTime = Math.max(Math.floor(duration / targetValue), 15);
          
          const timer = setInterval(() => {
            startValue += Math.ceil(targetValue / (duration / stepTime));
            if (startValue >= targetValue) {
              target.textContent = targetValue + suffix;
              clearInterval(timer);
            } else {
              target.textContent = startValue + suffix;
            }
          }, stepTime);
          
          observer.unobserve(target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(counter => counterObserver.observe(counter));
  }

  // ─── Reveal on Scroll ──────────────────────────────────────────────────────
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if (reveals.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    reveals.forEach(el => revealObserver.observe(el));
  }

  // ─── Back to Top Button ────────────────────────────────────────────────────
  const btt = document.getElementById('back-to-top');
  if (btt) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 300) {
        btt.classList.add('show');
      } else {
        btt.classList.remove('show');
      }
    });

    btt.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ─── Mobile HMS Sidebar Toggle ─────────────────────────────────────────────
  const toggleBtn = document.getElementById('hmsSidebarToggle');
  const sidebar = document.querySelector('.hms-sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    // Close when clicking outside
    document.addEventListener('click', function(e) {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== toggleBtn) {
        sidebar.classList.remove('open');
      }
    });
  }
});
