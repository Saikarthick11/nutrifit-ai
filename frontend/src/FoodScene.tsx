import { useState } from 'react';

/** A little optional delight; never changes or logs food. */
export function FoodScene() {
  const [playing, setPlaying] = useState(false);
  return <button type="button" className={'food-scene'+(playing?' is-playing':'')} aria-label="Play food illustration animation" onClick={()=>setPlaying(true)} onAnimationEnd={()=>setPlaying(false)}>
    <svg viewBox="0 0 260 150" aria-hidden="true">
      <ellipse cx="135" cy="130" rx="103" ry="12" fill="#ecd7bd" opacity=".5"/>
      <g className="food-toast"><path d="M35 112V65C15 42 39 24 65 30c28-9 54 14 33 35v47Z" fill="#d38b46" stroke="#814727" strokeWidth="3"/><path d="M44 104V61C29 46 48 36 65 41c20-6 38 7 24 20v43Z" fill="#ffe5ad"/><ellipse cx="67" cy="76" rx="18" ry="22" fill="#fffaf0"/><circle cx="68" cy="76" r="11" fill="#f4aa28"/></g>
      <g className="food-orange"><circle cx="139" cy="92" r="36" fill="#e97831"/><circle cx="139" cy="92" r="29" fill="#fff1cb"/><circle cx="139" cy="92" r="24" fill="#f7ab45"/><path d="M139 68v48m-24-24h48m-41-17 34 34m0-34-34 34" stroke="#fff1cb" strokeWidth="3"/><path d="M141 52q7-23 24-16-4 19-24 16" fill="#a26636"/></g>
      <g className="food-berry"><path d="M183 76q-16 4-13 20 5 20 25 32 24-16 28-35 2-19-21-18Z" fill="#b74261"/><path d="m178 76 12-12 6 10 13-10 0 13 12 3-20 6Z" fill="#784243"/><path d="m183 94 2 4m17-5 2 4m-10 12 2 4m17-12 2 4" stroke="#ffe2b7" strokeWidth="3" strokeLinecap="round"/></g>
      <g fill="#b74261"><path d="m112 21 3 7 7 3-7 3-3 7-3-7-7-3 7-3Z"/><circle cx="230" cy="56" r="4"/><circle cx="24" cy="94" r="3"/></g>
    </svg>
    <span>A little zest for your day <span aria-hidden="true">↗</span></span>
  </button>;
}
