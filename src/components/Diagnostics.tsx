import { useLayoutEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { profile, scanImage, scanSteps } from '../config/content'

gsap.registerPlugin(ScrollTrigger)

// Закреплённая сцена: кадр раскрывается на всю ширину, затем по одной появляются точки проверки
export default function Diagnostics() {
  const root = useRef<HTMLElement>(null)
  const [step, setStep] = useState(-1)

  useLayoutEffect(() => {
    const n = scanSteps.length
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: root.current,
          start: 'top top',
          end: '+=' + (window.innerHeight * 2.4),
          pin: true,
          scrub: 0.6,
          onUpdate: (self) => {
            const p = (self.progress - 0.35) / 0.65
            setStep(p < 0 ? -1 : Math.min(n - 1, Math.floor(p * n)))
          },
        },
      })
      tl.fromTo('.diag-frame', { clipPath: 'inset(0% 16% 0% 16% round 28px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', duration: 0.35, ease: 'power2.inOut' })
        .fromTo('.diag-inner img', { scale: 1.15 }, { scale: 1, duration: 0.35, ease: 'power2.inOut' }, 0)
        .to('.diag-head', { opacity: 0.35, duration: 0.2 }, 0.15)
      scanSteps.forEach((_, i) => {
        tl.fromTo(`.spot-${i}`, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.08 }, 0.35 + (i * 0.65) / n)
      })
    }, root)
    return () => ctx.revert()
  }, [])

  const cur = scanSteps[step]

  return (
    <section className="diag" ref={root}>
      <div className="diag-head">
        <p className="kicker">{profile.scan.kicker}</p>
        <h2 className="h-l">{profile.scan.title[0]}<br />{profile.scan.title[1]}</h2>
      </div>
      <div className="diag-frame">
        <div className="diag-inner">
          <img src={scanImage} alt={profile.scan.alt} loading="lazy" />
          {scanSteps.map((s, i) => (
            <div key={s.title} className={'spot spot-' + i} style={{ left: s.x + '%', top: s.y + '%' }}>
              <i />
              <span>{s.title}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="diag-cap" aria-live="polite">
        {cur ? (
          <>
            <b>{cur.title}</b>
            <span>{cur.text}</span>
          </>
        ) : (
          <span>{profile.scan.idle}</span>
        )}
      </div>
    </section>
  )
}
