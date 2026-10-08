import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ChevronRight } from 'lucide-react'
import heroImg from '../assets/img/hero.webp'
import { site } from '../config/site'

gsap.registerPlugin(ScrollTrigger)

export default function Hero({ ready }: { ready: boolean }) {
  const root = useRef<HTMLElement>(null)
  const img = useRef<HTMLImageElement>(null)

  useEffect(() => {
    if (!ready) return
    const ctx = gsap.context(() => {
      // медленный «наезд» камеры и последовательное появление текста
      gsap.fromTo(img.current, { scale: 1.12 }, { scale: 1, duration: 2.6, ease: 'power2.out' })
      gsap.fromTo('.hero [data-in]', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 1.1, stagger: 0.09, ease: 'power3.out', delay: 0.25 })
      // при прокрутке фото уходит медленнее текста
      gsap.to(img.current, { yPercent: 12, ease: 'none', scrollTrigger: { trigger: root.current, start: 'top top', end: 'bottom top', scrub: true } })
      gsap.to('.hero-body', { opacity: 0, y: -40, ease: 'none', scrollTrigger: { trigger: root.current, start: '30% top', end: '80% top', scrub: true } })
    }, root)
    return () => ctx.revert()
  }, [ready])

  return (
    <section id="top" className="hero" ref={root}>
      <div className="hero-media">
        <img ref={img} src={heroImg} alt="Автомобиль в тёмном сервисном боксе" fetchPriority="high" />
      </div>
      <div className="hero-beam" aria-hidden="true" />
      <div className="wrap hero-body">
        <div className="hero-row">
          <div>
            <p className="kicker" data-in>{site.name} · {site.city}</p>
            <h1 className="h-xl" data-in>Автосервис<br />в {site.cityIn}.</h1>
            <p className="hero-sub" data-in>Профессиональное обслуживание вашего автомобиля. Диагностика, ремонт и ТО с гарантией на выполненные работы.</p>
            <div className="hero-cta" data-in>
              <a className="btn btn-blue" href="#contact">Записаться на сервис</a>
              <a className="link" href="#services">Наши услуги <ChevronRight /></a>
            </div>
          </div>
          <div className="hero-facts" data-in>
            <span><b>{site.city}</b> · {site.address.replace(/^г\.\s*\S+,\s*/, '')}</span>
            <span><b>Профессиональный сервис</b> с {site.since} года</span>
            <span><b>Гарантия {site.warrantyMonths} мес.</b> на все работы</span>
          </div>
        </div>
      </div>
    </section>
  )
}
