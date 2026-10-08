import { useCallback, useEffect, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Loader from './components/Loader'
import Nav from './components/Nav'
import Hero from './components/Hero'
import Statement from './components/Statement'
import Highlights from './components/Highlights'
import Diagnostics from './components/Diagnostics'
import Numbers from './components/Numbers'
import Works from './components/Works'
import Reviews from './components/Reviews'
import Booking from './components/Booking'
import Footer from './components/Footer'
import { profile } from './config/profiles'

gsap.registerPlugin(ScrollTrigger)

export default function App() {
  const [ready, setReady] = useState(false)
  const onDone = useCallback(() => setReady(true), [])

  // Спокойное появление: короткий подъём и проявление, без размытия
  useEffect(() => {
    if (!ready) return
    const ctx = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>('[data-reveal]').forEach((el) => {
        gsap.fromTo(el, { opacity: 0, y: 32 }, {
          opacity: 1, y: 0, duration: 1, ease: 'power3.out',
          delay: Number(el.dataset.delay ?? 0),
          clearProps: 'transform',
          scrollTrigger: { trigger: el, start: 'top 90%', once: true },
        })
      })
    })
    const t = setTimeout(() => ScrollTrigger.refresh(), 300)
    return () => { clearTimeout(t); ctx.revert() }
  }, [ready])

  return (
    <>
      <Loader onDone={onDone} />
      <Nav />
      <main>
        <Hero ready={ready} />
        <Statement />
        <Highlights />
        <Diagnostics />
        <Numbers />
        {profile.works && <Works />}
        {profile.reviews && <Reviews />}
        <Booking />
      </main>
      <Footer />
    </>
  )
}
