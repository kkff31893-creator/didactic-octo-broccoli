import { useLayoutEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { statement } from '../config/content'

gsap.registerPlugin(ScrollTrigger)

// Слова проявляются из серого в белый по мере прокрутки
export default function Statement() {
  const root = useRef<HTMLElement>(null)

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      gsap.to('.w', {
        opacity: 1,
        stagger: 0.1,
        ease: 'none',
        scrollTrigger: { trigger: root.current, start: 'top 75%', end: 'bottom 55%', scrub: 0.6 },
      })
    }, root)
    return () => ctx.revert()
  }, [])

  return (
    <section className="statement" id="about" ref={root}>
      <div className="wrap">
        <p>
          {statement.split(' ').map((w, i) => (
            <span key={i} className="w">{w} </span>
          ))}
        </p>
      </div>
    </section>
  )
}
