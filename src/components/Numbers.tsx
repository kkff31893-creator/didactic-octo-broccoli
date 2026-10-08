import { useLayoutEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ChevronRight } from 'lucide-react'
import { profile } from '../config/profiles'

gsap.registerPlugin(ScrollTrigger)

const fmt = (n: number, d = 0) => n.toLocaleString('ru-RU', { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/ /g, ' ')

export default function Numbers() {
  const root = useRef<HTMLElement>(null)
  const stats = profile.stats
  const wide = window.matchMedia('(min-width: 961px)').matches

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      root.current?.querySelectorAll<HTMLElement>('[data-count]').forEach((el) => {
        const o = { v: 0 }
        const target = Number(el.dataset.count)
        const d = Number(el.dataset.dec ?? 0)
        gsap.to(o, {
          v: target,
          duration: 1.8,
          ease: 'power3.out',
          onUpdate: () => { el.textContent = fmt(o.v, d) },
          scrollTrigger: { trigger: el, start: 'top 85%', once: true },
        })
      })
    }, root)
    return () => ctx.revert()
  }, [])

  if (!stats) return null

  return (
    <section className="numbers" id="why" ref={root}>
      <div className="wrap">
        <div data-reveal>
          <p className="kicker">{stats.kicker}</p>
          <h2 className="h-l">{stats.title[0]}<br />{stats.title[1]}</h2>
        </div>
        <div className="num-grid" style={wide ? { gridTemplateColumns: `repeat(${stats.items.length}, 1fr)` } : undefined}>
          {stats.items.map((s, i) => (
            <div className="num" key={s.label} data-reveal data-delay={i * 0.08}>
              <b><span data-count={s.value} data-dec={s.decimals ?? 0}>{fmt(0, s.decimals)}</span><small>{s.suffix}</small></b>
              <span>{s.label}</span>
            </div>
          ))}
        </div>
        {stats.link && (
          <a className="link" href={stats.link.href} target="_blank" rel="noopener noreferrer" style={{ marginTop: 48 }} data-reveal>
            {stats.link.text} <ChevronRight />
          </a>
        )}
      </div>
    </section>
  )
}
