import { useLayoutEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { stats } from '../config/content'

gsap.registerPlugin(ScrollTrigger)

const fmt = (n: number) => Math.round(n).toLocaleString('ru-RU').replace(/ /g, ' ')

export default function Numbers() {
  const root = useRef<HTMLElement>(null)

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      root.current?.querySelectorAll<HTMLElement>('[data-count]').forEach((el) => {
        const o = { v: 0 }
        const target = Number(el.dataset.count)
        gsap.to(o, {
          v: target,
          duration: 1.8,
          ease: 'power3.out',
          onUpdate: () => { el.textContent = fmt(o.v) },
          scrollTrigger: { trigger: el, start: 'top 85%', once: true },
        })
      })
    }, root)
    return () => ctx.revert()
  }, [])

  return (
    <section className="numbers" id="why" ref={root}>
      <div className="wrap">
        <div data-reveal>
          <p className="kicker">Почему выбирают нас</p>
          <h2 className="h-l">Надёжность,<br />проверенная временем.</h2>
        </div>
        <div className="num-grid">
          {stats.map((s, i) => (
            <div className="num" key={s.label} data-reveal data-delay={i * 0.08}>
              <b><span data-count={s.value}>0</span><small>{s.suffix}</small></b>
              <span>{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
