import { works } from '../config/content'

export default function Works() {
  return (
    <section className="works" id="works">
      <div className="wrap">
        <div data-reveal>
          <p className="kicker">Наши работы</p>
          <h2 className="h-l">Работы, за которые<br />не стыдно.</h2>
        </div>
        <div className="work-grid">
          {works.map((w, i) => (
            <article className="work" key={w.title} data-reveal data-delay={(i % 2) * 0.1}>
              <div className="work-img"><img src={w.img} alt={w.title} loading="lazy" /></div>
              <small>{w.tag}</small>
              <h3>{w.title}</h3>
              <p>{w.text}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
