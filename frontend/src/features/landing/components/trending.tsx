const TrendingMovies = () => {
  return (
    <section className="bg-background-dark py-24">
      <div className="max-w-300 mx-auto px-6">
        <div className="flex items-center justify-between mb-10">
          <h2 className="text-white text-3xl font-bold tracking-tight">
            Trending Now
          </h2>
          <button className="text-primary font-bold flex items-center gap-1 hover:underline">
            Explore all{' '}
            <span className="material-symbols-outlined text-sm!">
              arrow_forward_ios
            </span>
          </button>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          <div className="group relative aspect-[3/4.5] overflow-hidden rounded-lg bg-white/5 shadow-2xl">
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
              data-alt="Sci-fi movie poster with glowing blue portal"
              style={{
                backgroundImage:
                  "url('https://lh3.googleusercontent.com/aida-public/AB6AXuA664CmI8OeedaN5rbc2SnWrr4n1mgtaF14fsYQDiERY7kQDzxSd7OCzxGfdAnWNihvG7PNM8LGXTUdEAj3J4BCJqQRM-5k10UrUPTCtgqbM1DPcuanKEmSiz4dxNrp0MvaNSmF_Uz6Oj7kUccv2cO7HqnDgsYDjD0-Gh9byAK0VohdX_EsIAZ1nPSpX7uK7JCsAr4S8_xauy-rsnqFXvoNVR3y7NG1gTpc0k3nWDqefgfUGClF6JWjFYR6DWgNgd4Wt1d3v6gdLBw')",
              }}
            ></div>
            <div className="absolute inset-0 bg-linear-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
              <p className="text-white font-bold text-sm">
                Interstellar Journey
              </p>
            </div>
          </div>
          <div className="group relative aspect-[3/4.5] overflow-hidden rounded-lg bg-white/5 shadow-2xl">
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
              data-alt="Noir style movie poster detective in rain"
              style={{
                backgroundImage:
                  'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCDXhE8CVlUBMDtP5SDr7H4P8dVSGlEvBw2u_URCPfDJ7aEAbLt4-L9MICMZ1COSYzP01zlXNiMbSktmyW6u2FijweZa_4rNI5FWQ3G9ZT1DL8Hz8cjYXUlxfHOCCtmK-AzBYYS2fUQ9oGuNdu9sMreA2JIZeNaoCD9k9W-NXDceiehFmIE98oSg1PK9OyZUV6mjmaJfvo6PMuXntFZ5uLqzdRNOgPartEYQpWzCuONks5S5hrY41gwHuuyapnhskQbRGQ9XblRMDg")',
              }}
            ></div>
            <div className="absolute inset-0 bg-linear-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
              <p className="text-white font-bold text-sm">Midnight Case</p>
            </div>
          </div>
          <div className="group relative aspect-[3/4.5] overflow-hidden rounded-lg bg-white/5 shadow-2xl">
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
              data-alt="Colorful abstract animated movie poster"
              style={{
                backgroundImage:
                  "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAQ_zQDld3YHeczctlWHWy5_9kJPiUtOUpJ44F-37LDLtc2-3-NkWT6OMeVpK-wTUfKgp3DoMDrDMUwA6MJpdpc1CNOYKOfJw6-DmkIZ-0EA1e4ZKrbUuGlcScSpkHMX4TjmhqMqTG5zr5tjlLWjQEe79DjhHP171Wg66JNSeBAhjKP4E91om70_INIHYBdZgrz9EouFrfQiqUh51IEpyWh45vlc6-vuS9HyN9cFrP0hlii6p7cH89_10pdqgrKrSG6G_zrzBSyKiY')",
              }}
            ></div>
            <div className="absolute inset-0 bg-linear-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
              <p className="text-white font-bold text-sm">Neon World</p>
            </div>
          </div>
          <div className="group relative aspect-[3/4.5] overflow-hidden rounded-lg bg-white/5 shadow-2xl">
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
              data-alt="Nature documentary poster with mountains"
              style={{
                backgroundImage:
                  "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCo_oHd_Q8lw1gVg4mAnFNgvcpArDnhAQ93hAbyIwH77re6XU-AKsc2NdD8brDIf_ztwBVaQr93UfBP-HV_DcqGHH4jsFTfIuTnhO6EGFZXZ5whVT67tPEOaICeSu2ByyijLRTlVHZiXP5mTICyJmfdZfyyDA0Cq-d9SomckMGXESxE2zCPmTrx-_mMbY5sfeNGN17e22-7PuUxtagi_8GqqVEuYoPCUyv9RunEu9Rsc41MxTfMPtV55nUNloXxuj1cXw89rhY40_8')",
              }}
            ></div>
            <div className="absolute inset-0 bg-li-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
              <p className="text-white font-bold text-sm">Peak of Silence</p>
            </div>
          </div>
          <div className="group relative aspect-[3/4.5] overflow-hidden rounded-lg bg-white/5 shadow-2xl">
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
              data-alt="Action movie poster with fast car"
              style={{
                backgroundImage:
                  "url('https://lh3.googleusercontent.com/aida-public/AB6AXuA4f8Z3cOaHWEwKC2jmkzS6jfoBqjDmtYkzgMJgiFtoygYZoWhoKe66uxD-juDKfbzHKwG5BNm5wJL4uCcbzhVIZTo2BOqVb7aOYmwp6CcJ7B6BynyEPH4FiEUDo9AYnVIkvrOGxl7VQo7iLyVcJv_iMuD5VXPs4rpH5g1tFmdY3gdq8Ay843iiOFjDT4dOi-LmJJWYatDkRIdL635Re4kDk-QPTbSCNGlkdkeZ8rk-yv8Hz3t1liQTnfWBkCuLY78ZVsDzArZs3Sw')",
              }}
            ></div>
            <div className="absolute inset-0 bg-linear-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
              <p className="text-white font-bold text-sm">Velocity X</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default TrendingMovies
